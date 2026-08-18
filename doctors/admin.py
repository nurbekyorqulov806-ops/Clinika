from django.contrib import admin
from .models import Department, DoctorProfile, Review


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'department', 'experience_years', 'price', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'created_at')
    list_filter = ('rating',)
