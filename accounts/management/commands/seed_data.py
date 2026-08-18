"""
Namunaviy ma'lumotlar bilan bazani to'ldirish uchun buyruq.
Ishlatish: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from doctors.models import Department, DoctorProfile


DEPARTMENTS = [
    ("Kardiologiya", "bi-heart-pulse"),
    ("Nevrologiya", "bi-activity"),
    ("Stomatologiya", "bi-emoji-smile"),
    ("Pediatriya", "bi-balloon"),
    ("Dermatologiya", "bi-bandaid"),
    ("Oftalmologiya", "bi-eye"),
]

DOCTORS = [
    ("Aziz", "Karimov", "Kardiologiya", "Yurak-qon tomir kasalliklari mutaxassisi", 12, 150000),
    ("Dilnoza", "Yusupova", "Nevrologiya", "Bosh og'rig'i va nerv tizimi kasalliklari bo'yicha mutaxassis", 8, 130000),
    ("Sherzod", "Tashkentov", "Stomatologiya", "Tish davolash va protezlash bo'yicha mutaxassis", 6, 100000),
    ("Malika", "Rashidova", "Pediatriya", "Bolalar kasalliklari bo'yicha shifokor", 10, 90000),
    ("Bekzod", "Nurmatov", "Dermatologiya", "Teri kasalliklari bo'yicha mutaxassis", 5, 110000),
    ("Nilufar", "Ergasheva", "Oftalmologiya", "Ko'z kasalliklari bo'yicha mutaxassis", 9, 120000),
]


class Command(BaseCommand):
    help = "Bo'limlar, shifokorlar va demo bemor bilan bazani to'ldiradi."

    @transaction.atomic
    def handle(self, *args, **options):
        dept_map = {}
        for name, icon in DEPARTMENTS:
            dept, _ = Department.objects.get_or_create(name=name, defaults={'icon': icon})
            dept_map[name] = dept
        self.stdout.write(self.style.SUCCESS(f"{len(DEPARTMENTS)} ta bo'lim tayyor."))

        created_count = 0
        for idx, (first, last, dept_name, specialization, exp, price) in enumerate(DOCTORS, start=1):
            username = f"doctor{idx}"
            if User.objects.filter(username=username).exists():
                continue
            user = User.objects.create_user(
                username=username,
                password="doctor12345",
                first_name=first,
                last_name=last,
                email=f"{username}@medicare.uz",
                role=User.Role.DOCTOR,
                phone=f"+998 90 000 00 {idx:02d}",
            )
            DoctorProfile.objects.create(
                user=user,
                department=dept_map[dept_name],
                specialization=specialization,
                bio=f"{first} {last} — {specialization.lower()} sohasida {exp} yillik tajribaga ega.",
                experience_years=exp,
                price=price,
                schedule="Dush-Juma, 09:00-17:00",
                room_number=f"{100 + idx}",
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"{created_count} ta shifokor yaratildi. (parol: doctor12345)"))

        if not User.objects.filter(username='patient1').exists():
            User.objects.create_user(
                username='patient1', password='patient12345',
                first_name='Jasur', last_name='Alimov',
                email='patient1@medicare.uz', role=User.Role.PATIENT,
                phone='+998 90 111 22 33',
            )
            self.stdout.write(self.style.SUCCESS("Demo bemor yaratildi: patient1 / patient12345"))

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin', password='admin12345', email='admin@medicare.uz',
            )
            User.objects.filter(username='admin').update(role=User.Role.ADMIN)
            self.stdout.write(self.style.SUCCESS("Demo administrator yaratildi: admin / admin12345"))

        self.stdout.write(self.style.SUCCESS("Namunaviy ma'lumotlar muvaffaqiyatli yuklandi!"))
