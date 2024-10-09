from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Staff)
admin.site.register(Bed)
admin.site.register(Profile)
admin.site.register(NonStaff)
admin.site.register(KenyaHospitalData)
admin.site.register(NHIFPayment)
admin.site.register(TBPatient)