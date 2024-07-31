from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(EmergencyService)
admin.site.register(VolunteerOpportunity)
admin.site.register(Booking)
admin.site.register(Feedback)
admin.site.register(VolunteerApplication)