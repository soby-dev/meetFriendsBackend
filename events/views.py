from unicodedata import category
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from .models import Event, EventCategory, EventLike, EventParticipant
from rest_framework.decorators import parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import EventSerializer, EventUpdateSerializer,  EventCategorySerializer, EventParticipantSerializer
from .utils import event_code, latitude_longitude, getAddress
# from .permissions import EventOwnerPermission
from rest_framework import generics
from rest_framework.views import APIView
import ast
from .eventFilters import SerializeEvents, EventTownFilter, EventCodeSearch, EventDateFilter, EventPriceFilter, EventNameFilter, EventTagsFilter, EventStateFilter, EventCountryFilter, EventTagsFilter, EventsInteractedWith
from datetime import date, timedelta
from rest_framework import status


# Create your views here.
 # update a user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser, FileUploadParser])
def CreateEvent(request):

    '''only the serializer for the event model (EventSerializer) is being used. 
    more information than what is available on the model is being sent. 
    The rest of the information is being retrieved so they can be manually added to their respective models
    ''' 
    categories = request.data.getlist('category')


    # other data that has been retrieved needs to be removed from request.data. however, request.data is immutable so a copy of it is made. 
    # This copy is mutable
    data = request.data.copy()


    # data that has been stored in a variable is removed from the rest
    if categories: 
        data.pop('category')
    else:
        pass


    # create event code and check if it already exists in database as it won't be passed from frontend and it has to be unique.
    # update data with event code too
    code_exists = True
    code = ''
    while code_exists:
        code = event_code()
        event = Event.objects.filter(code=code)
        if not event:
            code_exists = False
            data.update({'code': code})
            code = code

    # get latitude and longitude of event location to add to data.
    address = data['address']
    state = data['state']
    country = data['country']

    try:
        latitude = round(float(latitude_longitude(address, state, country)['lat']), 5)
        longitude = round(float(latitude_longitude(address, state, country)['lng']), 5)
    except TypeError:
        return Response('The address was not found')

    data.update({'latitude': latitude, 'longitude': longitude})

    # the data that fits into EventSerializer is serialised and saved
    serializer = EventSerializer(data=data)

    if serializer.is_valid(raise_exception=True):
        obj = serializer.save(creator = request.user)
        EventParticipant.objects.create(event=obj, user=request.user)
    

    # get event that was just saved
    event = Event.objects.get(code=code)

    # add categories
    for category in categories:
        EventCategory.objects.create(event=event, category=category)



    return Response(serializer.errors)





# class to filter events and get the event
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
def GetEvent(request):

    user = request.user

    # check if user is trying to retrieve liked, joined or created events for his profile page
    interaction = request.data.get('interaction')
    
    # This is the user's current location.
    location = request.data.get('location')
    
    
    try:
        # change location string to dictionary
        location = ast.literal_eval(location)
        latitude = location['latitude']
        longitude = location['longitude']
        address = getAddress(latitude, longitude)
        UserCurrentState = address[0]['city']
        UserCurrentcountry = address[0]['country']
    except:
        pass

    code = request.data.get('code')
    town = request.data.get('town')
    country = request.data.get('country')
    state = request.data.get('state')
    price = request.data.get('price')
    minimum_price = request.data.get('minimumPrice')
    maximum_price = request.data.get('maximumPrice')
    dateFilter = request.data.get('date')


    start_date = request.data.get('startDate')
    end_date = request.data.get('endDate')
    
    if not dateFilter:
        start_date = date.today().strftime('%Y-%m-%d')
        end_date = date.today() + timedelta(days = 30)
        end_date = end_date.strftime('%Y-%m-%d')
        
    name = request.data.get('name')


    try:
        tags = request.data.getlist('category')
    except:
        tags=None

    
    eventList = []

    
    if code:
        event = EventCodeSearch(code)
        data = SerializeEvents(event, user)
        return Response(data)
    else:
        pass

    if date:
        event = EventDateFilter(start_date, end_date)
        eventList.append(event)
    else:
        pass

    if town:
        event = EventTownFilter(town).filter(date__range=[start_date, end_date])
        eventList.append(event)
    else:
        pass

    if country:
        event = EventCountryFilter(country).filter(date__range=[start_date, end_date])
        eventList.append(event)
    else:
        pass

    if price: 
        event = EventPriceFilter(minimum=minimum_price, maximum=maximum_price).filter(date__range=[start_date, end_date])
        eventList.append(event)
    else:
        pass


    if name: 
        event = EventNameFilter(name)
        eventList.append(event)
    else:
        pass

    if tags:
        event = EventTagsFilter(start_date, end_date, tags).filter(date__range=[start_date, end_date])
        eventList.append(event)
    else:
        pass


    if state:
        event = EventStateFilter(state, country).filter(date__range=[start_date, end_date])
        eventList.append(event)
    else:
        pass


    if eventList != []:
        events = ''
        # use counter to determine if it is the first event
        counter = 0
        for event in eventList:
            if counter == 0:
                # you need an event to do an intersection with as events is initially empty
                # if counter is zero (i.e this is the firt iteration), use the first event. 
                events = event
                counter += 1
            filter = event.intersection(events)
            events = filter

        data = SerializeEvents(events, request.user)
        print(f'xxxxxx{request.user}')
        return Response(data)
    else:
        return Response({}) 



# join an event
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def JoinEvent(request, eventcode):
    user = request.user

    event = Event.objects.get(code=eventcode)

    if event.signedUp == event.maxParticipants:
        return Response('event is already full!')
    
    # check if user has signedUp the event before so next click removes him
    hasSignedUp = EventParticipant.objects.filter(event=event, user=user)
    if hasSignedUp:
        data = {"signedUp": event.signedUp - 1}
        EventParticipant.objects.get(event=event, user=user).delete()
        joined = False
    else:
        data = {"signedUp": event.signedUp + 1}
        EventParticipant.objects.create(event=event, user=user)
        joined = True
    serializer = EventSerializer(instance=event, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()

    serializer_response = {'joined':joined}
    
    
    return Response(serializer_response)

