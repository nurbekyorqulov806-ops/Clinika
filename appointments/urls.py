from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/<int:doctor_id>/', views.book_appointment_view, name='book'),
    path('patient/', views.patient_dashboard_view, name='patient_dashboard'),
    path('patient/cancel/<int:pk>/', views.cancel_appointment_view, name='cancel'),
    path('patient/review/<int:pk>/', views.leave_review_view, name='leave_review'),
    path('patient/history/', views.medical_history_view, name='medical_history'),
    path('doctor/', views.doctor_dashboard_view, name='doctor_dashboard'),
    path('doctor/status/<int:pk>/<str:new_status>/', views.update_appointment_status_view, name='update_status'),
    path('doctor/record/<int:pk>/', views.add_medical_record_view, name='add_medical_record'),
]
