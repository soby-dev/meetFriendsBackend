from django.urls import path
from . import views

urlpatterns = [
    path('create-event/', views.CreateEvent, name='create-event'),
    path('get-event/', views.GetEvent, name='get-event'),
    path('join-event/<str:eventcode>', views.JoinEvent, name='join-event'),
] 