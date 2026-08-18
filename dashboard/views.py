from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from datetime import date, timedelta
import json

from accounts.models import User
from doctors.models import DoctorProfile, Department, Review
from appointments.models import Appointment


def _is_admin(user):
    return user.is_authenticated and user.is_admin_role


@login_required
@user_passes_test(_is_admin, login_url='home')
def admin_dashboard_view(request):
    total_patients = User.objects.filter(role=User.Role.PATIENT).count()
    total_doctors = User.objects.filter(role=User.Role.DOCTOR).count()
    total_appointments = Appointment.objects.count()
    completed_appointments = Appointment.objects.filter(status=Appointment.Status.COMPLETED)

    estimated_revenue = 0
    for appt in completed_appointments.select_related('doctor'):
        estimated_revenue += appt.doctor.price

    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']

    # So'nggi 6 oy bo'yicha navbatlar statistikasi (grafik uchun)
    six_months_ago = date.today() - timedelta(days=180)
    monthly = (
        Appointment.objects.filter(date__gte=six_months_ago)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    chart_labels = [m['month'].strftime('%Y-%m') for m in monthly]
    chart_data = [m['count'] for m in monthly]

    department_stats = (
        Department.objects.annotate(doctor_count=Count('doctors', distinct=True))
        .order_by('-doctor_count')
    )

    top_doctors = (
        DoctorProfile.objects.annotate(appt_count=Count('appointments'))
        .order_by('-appt_count')[:5]
    )

    recent_appointments = Appointment.objects.select_related('patient', 'doctor__user').order_by('-created_at')[:10]

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'completed_count': completed_appointments.count(),
        'pending_count': Appointment.objects.filter(status=Appointment.Status.PENDING).count(),
        'estimated_revenue': estimated_revenue,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'department_stats': department_stats,
        'top_doctors': top_doctors,
        'recent_appointments': recent_appointments,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
