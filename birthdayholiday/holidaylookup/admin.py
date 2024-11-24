from django.contrib import admin
from .models import SAIDRecord,PublicHoliday

# Register your models here.

admin.site.register(SAIDRecord)
admin.site.register(PublicHoliday)
