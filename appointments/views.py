from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date as date_cls

from doctors.models import DoctorProfile
from doctors.forms import ReviewForm
from .models import Appointment, MedicalRecord, LabResult
from .forms import AppointmentForm, MedicalRecordForm, LabResultForm


def _require_patient(user):
    if not user.is_patient_role:
        raise PermissionDenied("Bu sahifa faqat bemorlar uchun.")


def _require_doctor(user):
    if not user.is_doctor_role:
        raise PermissionDenied("Bu sahifa faqat shifokorlar uchun.")


@login_required
def book_appointment_view(request, doctor_id):
    _require_patient(request.user)

    doctor = get_object_or_404(
        DoctorProfile,
        pk=doctor_id,
        is_active=True
    )

    if request.method == 'POST':
        print("1. FORM YARATILDI")

        form = AppointmentForm(request.POST)

        if form.is_valid():
            print("2. FORM VALID")

            appointment = form.save(commit=False)

            print("3. FORM SAVE BO'LDI")

            appointment.doctor = doctor
            appointment.patient = request.user

            print("4. DOCTOR BERILDI:", appointment.doctor)

            if Appointment.objects.filter(
                doctor=doctor,
                date=appointment.date,
                time=appointment.time
            ).exists():
                messages.error(
                    request,
                    "Bu vaqt band. Boshqa vaqt tanlang."
                )
            else:
                appointment.save()

                messages.success(
                    request,
                    "Navbatga muvaffaqiyatli yozildingiz!"
                )

                return redirect(
                    'appointments:patient_dashboard'
                )

    else:
        form = AppointmentForm()

    return render(
        request,
        'appointments/book_appointment.html',
        {
            'form': form,
            'doctor': doctor
        }
    )



@login_required
def patient_dashboard_view(request):
    _require_patient(request.user)
    today = date_cls.today()
    appointments = Appointment.objects.filter(patient=request.user).select_related('doctor__user')
    upcoming = appointments.filter(date__gte=today).exclude(status=Appointment.Status.CANCELLED)
    history = appointments.filter(Q(date__lt=today) | Q(status=Appointment.Status.COMPLETED))
    lab_results = LabResult.objects.filter(patient=request.user)

    context = {
        'upcoming': upcoming,
        'history': history,
        'lab_results': lab_results,
    }
    return render(request, 'appointments/patient_dashboard.html', context)


@login_required
def cancel_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
    if appointment.status in (Appointment.Status.PENDING, Appointment.Status.CONFIRMED):
        appointment.status = Appointment.Status.CANCELLED
        appointment.save()
        messages.info(request, "Navbat bekor qilindi.")
    return redirect('appointments:patient_dashboard')


@login_required
def leave_review_view(request, pk):
    _require_patient(request.user)
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user, status=Appointment.Status.COMPLETED)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor = appointment.doctor
            review.patient = request.user
            try:
                review.save()
                messages.success(request, "Sharh uchun rahmat!")
            except Exception:
                messages.error(request, "Siz bu shifokorga allaqachon baho bergansiz.")
    return redirect('appointments:patient_dashboard')


@login_required
def doctor_dashboard_view(request):
    _require_doctor(request.user)
    doctor_profile = request.user.doctor_profile
    today = date_cls.today()

    appointments = Appointment.objects.filter(doctor=doctor_profile).select_related('patient')
    today_appointments = appointments.filter(date=today).exclude(status=Appointment.Status.CANCELLED)
    upcoming = appointments.filter(date__gt=today).exclude(status=Appointment.Status.CANCELLED)
    pending = appointments.filter(status=Appointment.Status.PENDING)

    context = {
        'doctor_profile': doctor_profile,
        'today_appointments': today_appointments,
        'upcoming': upcoming,
        'pending': pending,
        'total_patients': appointments.values('patient').distinct().count(),
    }
    return render(request, 'appointments/doctor_dashboard.html', context)


@login_required
def update_appointment_status_view(request, pk, new_status):
    _require_doctor(request.user)
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user.doctor_profile)
    valid_statuses = dict(Appointment.Status.choices)
    if new_status in valid_statuses:
        appointment.status = new_status
        appointment.save()
        messages.success(request, f"Holat yangilandi: {valid_statuses[new_status]}")
    return redirect('appointments:doctor_dashboard')


@login_required
def add_medical_record_view(request, pk):
    _require_doctor(request.user)
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user.doctor_profile)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=getattr(appointment, 'medical_record', None))
        if form.is_valid():
            record = form.save(commit=False)
            record.appointment = appointment
            record.save()
            appointment.status = Appointment.Status.COMPLETED
            appointment.save()
            messages.success(request, "Tashxis va retsept saqlandi. Qabul yakunlandi.")
            return redirect('appointments:doctor_dashboard')
    else:
        form = MedicalRecordForm(instance=getattr(appointment, 'medical_record', None))
    return render(request, 'appointments/medical_record_form.html', {'form': form, 'appointment': appointment})


@login_required
def medical_history_view(request):
    _require_patient(request.user)
    records = MedicalRecord.objects.filter(appointment__patient=request.user).select_related(
        'appointment__doctor__user'
    )
    return render(request, 'appointments/medical_history.html', {'records': records})
