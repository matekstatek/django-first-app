from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils import timezone as tz, dateformat
from PIL import Image



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # nadpisanie metody w celu manipulacji wielkością obrazka
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# klasa zbierająca logi z logowań
class AuditEntry(models.Model):
    time = models.DateTimeField(default=tz.now)
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def has_change_permission(self, request, obj=None):
        return False

    # zwraca powyżej zebrane dane użytkownika
    def __unicode__(self):
        return f'{self.action} - {self.username} - {self.ip}'
    def __str__(self):
        return f'{self.action} - {self.username} - {self.ip}'

# zbieranie informacji gdy użytkownik się zalogował, wylogował lub nie
# udało mu się zalogować
@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(time=dateformat.format(tz.now(), 'Y-m-d H:i:s'), action='user_logged_in', ip=ip, username=user.username)

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(time=dateformat.format(tz.now(), 'Y-m-d H:i:s'), action='user_logged_out', ip=ip, username=user.username)

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    AuditEntry.objects.create(time=dateformat.format(tz.now(), 'Y-m-d H:i:s'), action='user_login_failed', username=credentials.get('username', None))
