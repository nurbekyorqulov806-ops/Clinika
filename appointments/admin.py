from django.contrib import admin
from .models import Appointment, MedicalRecord, LabResult


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__user__first_name')


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'created_at')


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'uploaded_at')
