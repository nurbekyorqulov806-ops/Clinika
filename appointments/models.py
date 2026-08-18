from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from doctors.models import DoctorProfile


class Appointment(models.Model):
    """Bemorning shifokorga yozilgan navbati."""

    class Status(models.TextChoices):
        PENDING = 'pending', "Kutilmoqda"
        CONFIRMED = 'confirmed', "Tasdiqlangan"
        COMPLETED = 'completed', "Yakunlangan"
        CANCELLED = 'cancelled', "Bekor qilingan"

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='appointments_as_patient')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(verbose_name="Sana")
    time = models.TimeField(verbose_name="Vaqt")
    reason = models.CharField(max_length=255, blank=True, verbose_name="Murojaat sababi")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Navbat"
        verbose_name_plural = "Navbatlar"
        ordering = ['-date', '-time']
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"{self.patient} -> {self.doctor} ({self.date} {self.time})"

    def clean(self):
        if self.doctor and not self.doctor.is_active:
            raise ValidationError("Bu shifokor hozircha faol emas.")


class MedicalRecord(models.Model):
    """Yakunlangan qabul asosida yoziladigan tashxis va retsept."""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_record')
    diagnosis = models.TextField(verbose_name="Tashxis")
    prescription = models.TextField(blank=True, verbose_name="Retsept / tavsiyalar")
    notes = models.TextField(blank=True, verbose_name="Qo'shimcha izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tibbiy karta yozuvi"
        verbose_name_plural = "Tibbiy karta yozuvlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"Tashxis: {self.appointment}"


class LabResult(models.Model):
    """Bemorning laboratoriya tahlil natijasi (fayl sifatida yuklanadi)."""
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_results')
    title = models.CharField(max_length=150, verbose_name="Tahlil nomi")
    file = models.FileField(upload_to='lab_results/', verbose_name="Fayl")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Laboratoriya natijasi"
        verbose_name_plural = "Laboratoriya natijalari"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.patient})"
