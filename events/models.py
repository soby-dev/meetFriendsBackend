from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

# Create your models here.

# This model is for events
class Event(models.Model):

    def current_time():
        time = datetime.now().strftime("%H:%M:%S")
        return time

    def current_date():
        date = date.today().strftime("%Y-%m-%d")
        return date

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=40)
    description = models.TextField(blank=False, max_length=2000)
    address = models.CharField(max_length = 100)
    town = models.CharField(max_length = 100, default = 'Portsmouth')
    country = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    date = models.DateField(default=current_date)
    time = models.TimeField(default=current_time)
    latitude = models.DecimalField(decimal_places=5, max_digits=20)
    longitude = models.DecimalField(decimal_places=5, max_digits=20)
    maxParticipants = models.IntegerField(default=2)
    signedUp = models.IntegerField(default=1)
    eventFull = models.BooleanField(default=False)
    eventComplete = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    dateTimeCreated = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    likes = models.IntegerField(default=0)
  

    def __str__(self):
        return f"{self.creator}'s {self.name} event"




# This model is to specify what category an event belongs to
class EventCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)

    # make it impossible to add the same category for an event twice 
    class Meta:
        unique_together = ['event', 'category']
        
    def __str__(self):
        return f"{self.event}: {self.category}"

        

# This model is to specify what users have joined an event
class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTimeCreated = models.DateTimeField(verbose_name='date created', auto_now_add=True)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user} attending {self.event}"



# this model is to specify which users like an event
class EventLike(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTimeCreated = models.DateTimeField(verbose_name='date created', auto_now_add=True)

    class Meta:
        unique_together = ['event', 'likedBy']    

    def __str__(self):
        return f"{self.likedBy} liked {self.event}"