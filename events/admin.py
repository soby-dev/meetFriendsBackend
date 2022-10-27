from django.contrib import admin
from .models import Event, EventCategory, EventLike, EventParticipant

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('creator', 'code', 'name', 'date', 'eventFull', 'eventComplete')
    search_fields = ('name', 'code')
    readonly_fields = ('creator', 'code', 'eventFull', 'eventComplete')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('event', 'category')
    search_fields = ('event', 'category')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



class EventLikeAdmin(admin.ModelAdmin):
    list_display = ('event', 'likedBy')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'user')
    search_fields = ('event', 'user')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(EventLike, EventLikeAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
