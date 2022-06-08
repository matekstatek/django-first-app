from django.db import models
from django.utils import timezone as tz
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    # dane postu: tytuł, treść, data postowania (domyślnie - teraz),
    # autor (pobrany z User, jeśli użytkownik zostanie usunięty to jego
    # posty również)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=tz.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # pobieranie pełnej ścieżki dla postu o konkretnym pk (private key)
    # - dzięki temu można usuwać konkretne posty znajdujące się w
    # localhost:8000/post/<int>
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
