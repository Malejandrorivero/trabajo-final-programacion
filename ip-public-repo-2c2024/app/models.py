from django.db import models
from django.conf import settings

class Favourite(models.Model):
    url = models.TextField()
    name = models.CharField(max_length=200)
    status = models.TextField()
    last_location = models.TextField()
    first_seen = models.TextField()
    comment = models.TextField(blank=True, null=True)  # Añadimos el campo de comentario

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'url', 'name', 'status', 'last_location', 'first_seen'),)
