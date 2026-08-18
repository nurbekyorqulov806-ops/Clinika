from django.conf import settings
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Department(models.Model):
    """Klinika bo'limi (masalan: Kardiologiya, Stomatologiya)."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    icon = models.CharField(max_length=50, default='bi-heart-pulse',
                             help_text="Bootstrap Icons nomi, masalan: bi-heart-pulse")
    description = models.TextField(blank=True, verbose_name="Tavsif")

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"
        ordering = ['name']

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    """Shifokorga tegishli qo'shimcha ma'lumotlar."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='doctor_profile', limit_choices_to={'role': 'doctor'})
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,
                                    related_name='doctors', verbose_name="Bo'lim")
    specialization = models.CharField(max_length=150, verbose_name="Mutaxassislik")
    bio = models.TextField(blank=True, verbose_name="Tavsif / tarjimai hol")
    experience_years = models.PositiveSmallIntegerField(default=0, verbose_name="Ish tajribasi (yil)")
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0,
                                 verbose_name="Qabul narxi (so'm)")
    schedule = models.CharField(max_length=255, blank=True,
                                 verbose_name="Ish jadvali", help_text="Masalan: Dush-Juma, 09:00-17:00")
    room_number = models.CharField(max_length=20, blank=True, verbose_name="Xona raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Shifokor profili"
        verbose_name_plural = "Shifokor profillari"
        ordering = ['-experience_years']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} — {self.specialization}"

    def get_absolute_url(self):
        return reverse('doctors:detail', kwargs={'pk': self.pk})

    @property
    def average_rating(self):
        agg = self.reviews.aggregate(models.Avg('rating'))
        avg = agg['rating__avg']
        return round(avg, 1) if avg else None

    @property
    def review_count(self):
        return self.reviews.count()


class Review(models.Model):
    """Bemorning shifokorga bergan bahosi va sharhi."""
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='reviews')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, verbose_name="Sharh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ['-created_at']
        unique_together = ('doctor', 'patient')

    def __str__(self):
        return f"{self.patient} -> {self.doctor} ({self.rating}/5)"
