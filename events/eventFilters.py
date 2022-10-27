# Default timeline
# 1. Show event friends created, liked 
# 2. Show event your groups created
# 3. popular events in your city.
# 4. Filter by date created.

from .models import Event, EventCategory, EventLike, EventParticipant
from django.contrib.auth.models import User
from .serializers import EventSerializer, EventCategorySerializer, EventParticipantSerializer, EventLikeSerializer



def EventCodeSearch(code):
    '''Function retrieves searches by event code'''

    event = Event.objects.filter(code__icontains=code)

    return(event)




def EventDateFilter(start_date, end_date, queryset=[]):
    '''Function to retrieve searches by event date'''
    event = Event.objects.filter(date__range=[start_date, end_date])

    return(event)


def EventPriceFilter(minimum, maximum):
    '''Function to retrieve event searches by price'''
    minimum = float(minimum)
    maximum = float(maximum)

    event = Event.objects.filter(price__gte = minimum, price__lte=maximum)

    return(event)



def EventStateFilter(state, country):
    '''Function to retrieve events by city'''

    event = Event.objects.filter(state__icontains=state, country__icontains=country)

    return(event)


def EventCountryFilter(country):
    '''Function to retrieve events by country'''

    event = Event.objects.filter(country__icontains= country)

    return(event)


def EventTownFilter(town):
    '''Function to retrieve events by town'''

    event = Event.objects.filter(town__icontains= town)

    return(event)    



def EventNameFilter(name):
    '''Function to retrieve events by country'''

    event = Event.objects.filter(name__icontains=name)

    return(event)


def EventTagsFilter(start_date, end_date, categories=[]):
    '''Function to retrieve events by categories'''

    tag_list = EventCategory.objects.filter(category__in=categories).values_list(
        'event', flat=True)

    events = Event.objects.filter(id__in = tag_list)
    events = events.filter(date__range=[start_date, end_date])

    return(events)


# def GetEventOnInterest(userId, start_date, end_date, interests=[]):
#     '''function to retrieve events based on users interest'''

#     user = User.objects.get(username=userId)

#     # if interest search is to be done based on users saved interests
#     if interests == []:
#         interests = Interest.objects.filter(user=user).values_list('interest')

#     # if interest search is to be done based on some interests the user has just provided.
    
#     events = EventCategory.objects.filter(category__in = interests)
#     events = Event.objects.filter(id__in = events)
#     events = events.filter(date__range=[start_date, end_date]).order_by('-dateTimeCreated')

#     return (events)


# get events user has either liked, is attending or created
def EventsInteractedWith(user, interaction):

    user = User.objects.get(username=user)

    if interaction == 'like':
        liked = EventLike.objects.filter(likedBy=user).order_by('-dateTimeCreated').values_list('event')
        events = Event.objects.filter(id__in = liked).order_by('-dateTimeCreated')

    elif interaction == 'attending':
        attending = EventParticipant.objects.filter(user=user).order_by('-dateTimeCreated').values_list('event')
        events = Event.objects.filter(id__in = attending).order_by('-dateTimeCreated')

    elif interaction == 'created':
        events = Event.objects.filter(creator=user).order_by('-dateTimeCreated')

    return(events)



def SerializeEvents(events, user):
    '''
    This function serializes all the events with their acts, files, categories and participants into one json file so they can be 
    transferred to the frontend at the same time
    '''

    # user = User.objects.get(username=user)

    data = []

    for item in events:
        event = EventSerializer(item).data
        categories = item.eventcategory_set.all()
        participants = item.eventparticipant_set.all()


        liked = False
        joined = False
        category_list = []
        participant_list = []
        for category in categories:
            category = EventCategorySerializer(category).data
            category_list.append(category)
        for participant in participants:
            print(f'xxxxxxvvv{participant.user}')
            if participant.user == user:
                joined = True
            participant = EventParticipantSerializer(participant).data
            participant_list.append(participant)
        
        event_details = {}
        event_details['event'] = event
        event_details['categories'] = category_list
        event_details['participants'] = participant_list
        event_details['liked'] = liked
        event_details['joined'] = joined

        data.append(event_details)

    return(data)







 