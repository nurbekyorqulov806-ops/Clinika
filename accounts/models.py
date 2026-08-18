from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Tizimning barcha foydalanuvchilari: admin, shifokor, bemor."""

    class Role(models.TextChoices):
        ADMIN = 'admin', "Administrator"
        DOCTOR = 'doctor', "Shifokor"
        PATIENT = 'patient', "Bemor"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PATIENT)
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon raqami")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    address = models.CharField(max_length=255, blank=True, verbose_name="Manzil")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profil rasmi")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_doctor_role(self):
        return self.role == self.Role.DOCTOR

    @property
    def is_patient_role(self):
        return self.role == self.Role.PATIENT

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None
