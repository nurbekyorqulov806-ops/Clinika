from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import DoctorProfile, Department


def doctor_list_view(request):
    doctors = DoctorProfile.objects.filter(is_active=True).select_related('user', 'department')

    query = request.GET.get('q', '').strip()
    department_id = request.GET.get('department', '')

    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query)
        )
    if department_id:
        doctors = doctors.filter(department_id=department_id)

    paginator = Paginator(doctors, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'departments': Department.objects.all(),
        'query': query,
        'selected_department': department_id,
    }
    return render(request, 'doctors/doctor_list.html', context)


def doctor_detail_view(request, pk):
    doctor = get_object_or_404(DoctorProfile.objects.select_related('user', 'department'), pk=pk)
    reviews = doctor.reviews.select_related('patient').all()
    context = {'doctor': doctor, 'reviews': reviews}
    return render(request, 'doctors/doctor_detail.html', context)
