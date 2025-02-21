from django.contrib import admin
from .models import Emergency, EmergencyType, ResponseTeam, EmergencyContacts

admin.site.register(Emergency)
admin.site.register(EmergencyType)
admin.site.register(ResponseTeam)
admin.site.register(EmergencyContacts)