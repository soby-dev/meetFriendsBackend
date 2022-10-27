from rest_framework import serializers
from .models import Event, EventCategory, EventLike, EventParticipant


class EventSerializer(serializers.ModelSerializer):

    # used to declare this is a froeign key string related field so serializer can check in the foreign key database
    creator = serializers.StringRelatedField()
 
    # sets creator_picture 
    tags = serializers.ReadOnlyField()
    participants = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('dateTimeCreated', 'eventComplete', 'eventFull', 'dateTimeCreated')


class EventUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('address', 'country', 'state', 'date', 'time', 'maxParticipants', 'price', 'recurring', 'description', 'name')


 
class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'


class EventParticipantSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    # sets creator_picture 
    participants_picture = serializers.ReadOnlyField(source='participating_profile_pic')

    class Meta:
        model = EventParticipant
        fields = '__all__'

class EventLikeSerializer(serializers.ModelSerializer):

    likedBy = serializers.StringRelatedField()

    class Meta:
        model = EventLike
        fields = '__all__'