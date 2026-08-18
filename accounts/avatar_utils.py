"""
Foydalanuvchi uchun avtomatik avatar (ism harflaridan iborat, rangli doira) yaratish.
Tashqi internetga bog'liq bo'lmagan holda ishlaydi (Pillow yordamida).
"""
import io
import hashlib
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

PALETTE = [
    (0, 150, 136),   # teal
    (33, 150, 243),  # blue
    (156, 39, 176),  # purple
    (255, 87, 34),   # deep orange
    (76, 175, 80),   # green
    (63, 81, 181),   # indigo
    (0, 188, 212),   # cyan
    (233, 30, 99),   # pink
]


def _pick_color(seed_text):
    h = hashlib.md5(seed_text.encode('utf-8')).hexdigest()
    idx = int(h, 16) % len(PALETTE)
    return PALETTE[idx]


def _initials(first_name, last_name, username):
    first_name = (first_name or '').strip()
    last_name = (last_name or '').strip()
    if first_name and last_name:
        return (first_name[0] + last_name[0]).upper()
    if first_name:
        return first_name[:2].upper()
    return (username or '?')[:2].upper()


def generate_avatar_file(first_name, last_name, username, size=256):
    """Berilgan ism/familiya asosida rangli, harfli avatar rasm fayli qaytaradi."""
    initials = _initials(first_name, last_name, username)
    bg_color = _pick_color(username or initials)

    img = Image.new('RGB', (size, size), color=bg_color)
    draw = ImageDraw.Draw(img)

    font = None
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for path in font_candidates:
        try:
            font = ImageFont.truetype(path, size=int(size * 0.42))
            break
        except (OSError, IOError):
            continue
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initials, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    position = ((size - text_w) / 2 - bbox[0], (size - text_h) / 2 - bbox[1])
    draw.text(position, initials, fill=(255, 255, 255), font=font)

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    filename = f"{(username or 'user')}_avatar.png"
    return ContentFile(buffer.read(), name=filename)
