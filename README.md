# MediCare — Klinika boshqaruv tizimi (Django)

Bemorlar, shifokorlar va administrator uchun to'liq klinika boshqaruv platformasi.
Python + Django + MySQL asosida yozilgan.

## Imkoniyatlar

- **3 xil rol:** Bemor, Shifokor, Administrator — har birining o'z paneli
- **Avtomatik avatar generatsiyasi** — foydalanuvchi rasm yuklamasa, ismi harflaridan rangli avatar avtomatik yaratiladi (Pillow)
- **Shifokorlarni qidirish va filtrlash** — bo'lim va ism bo'yicha
- **Onlayn navbatga yozilish** — sana/vaqt tanlash, band vaqtlarni tekshirish
- **Bemor kabineti** — kelayotgan/o'tgan qabullar, navbatni bekor qilish
- **Shifokor kabineti** — kunlik qabullar, holatni yangilash, tashxis/retsept yozish
- **Tibbiy karta (Medical record)** — har bir yakunlangan qabul bo'yicha tashxis va retsept saqlanadi
- **Laboratoriya natijalari** — fayl yuklash va yuklab olish
- **Reyting va sharhlar** — bemorlar shifokorni baholaydi
- **Administrator paneli** — statistika, grafiklar (Chart.js), eng faol shifokorlar, taxminiy daromad
- **Zamonaviy, responsive dizayn** — Bootstrap 5 + maxsus CSS

## O'rnatish

### 1. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3. MySQL bazasini tayyorlash

MySQL serverga kiring va baza yarating:

```sql
CREATE DATABASE clinic_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. `.env` faylini sozlash

`.env.example` faylidan nusxa oling va o'z ma'lumotlaringizni kiriting:

```bash
cp .env.example .env
```

`.env` faylida:
```
SECRET_KEY=maxfiy-kalit
DEBUG=True
DB_NAME=clinic_db
DB_USER=root
DB_PASSWORD=sizning_parolingiz
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Migratsiyalarni bajarish

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Namunaviy ma'lumotlar bilan to'ldirish (ixtiyoriy, lekin tavsiya etiladi)

Bu buyruq 6 ta bo'lim, 6 ta shifokor, 1 ta demo bemor va 1 ta admin yaratadi:

```bash
python manage.py seed_data
```

Demo hisoblar:
| Rol | Login | Parol |
|---|---|---|
| Administrator | admin | admin12345 |
| Shifokor | doctor1 ... doctor6 | doctor12345 |
| Bemor | patient1 | patient12345 |

### 7. Superuser yaratish (agar seed_data ishlatmasangiz)

```bash
python manage.py createsuperuser
```

### 8. Serverni ishga tushirish

```bash
python manage.py runserver
```

Brauzerda oching: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin

## Loyiha tuzilishi

```
clinic_project/
├── clinic/            # Loyiha sozlamalari (settings, urls)
├── accounts/          # Foydalanuvchilar, autentifikatsiya, avatar generatsiya
├── doctors/           # Shifokorlar, bo'limlar, sharhlar
├── appointments/      # Navbatlar, tibbiy karta, lab natijalari
├── dashboard/         # Administrator statistikasi
├── templates/         # HTML shablonlar
├── static/            # CSS, JS
└── media/             # Yuklangan fayllar (avatar, lab natijalari)
```

## Keyingi qadamlar uchun g'oyalar

- Django REST Framework qo'shib, mobil ilova uchun API yaratish
- SMS/Email orqali navbat eslatmalari (Celery + Eskiz.uz yoki Twilio)
- Payme/Click orqali onlayn to'lov integratsiyasi
- Retseptni PDF formatida yuklab olish (ReportLab yoki WeasyPrint)
- Real vaqtli chat (Django Channels)

## Muallif eslatmasi

Loyiha o'quv/portfolio maqsadida yaratilgan namunaviy tizim. Production muhitida
ishlatishdan oldin `SECRET_KEY`ni almashtiring, `DEBUG=False` qiling va MySQL
foydalanuvchisiga minimal huquqlar bering.
