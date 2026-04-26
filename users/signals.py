from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from products.models import Cart

@receiver(post_save, sender=User)
def user_cart_creator(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)