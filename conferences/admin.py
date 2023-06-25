from django.contrib import admin
from conferences.models import Conference
from conferences.models import EventPlanner
from conferences.models import Speaker
from conferences.models import Session

# Register your models here.
admin.site.register(Conference)
admin.site.register(EventPlanner)
admin.site.register(Speaker)
admin.site.register(Session)
