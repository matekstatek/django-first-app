from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


log = logging.getLogger(__name__)

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    log.debug(f'login user: {user} via ip: {ip}')

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    log.debug(f'logout user: {user} via ip: {ip}')

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    log.warning(f'login failed for: {credentials}')
