from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .avatar_utils import generate_avatar_file


@receiver(post_save, sender=User)
def create_default_avatar(sender, instance, created, **kwargs):
    """Yangi foydalanuvchi uchun agar avatar yuklanmagan bo'lsa, avtomatik yaratiladi."""
    if created and not instance.avatar:
        avatar_file = generate_avatar_file(instance.first_name, instance.last_name, instance.username)
        instance.avatar.save(avatar_file.name, avatar_file, save=True)
