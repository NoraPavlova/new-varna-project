from django.contrib import admin
from . models import User, Cause, Event, Tag, Comment


admin.site.register(User)
admin.site.register(Cause)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(Comment)