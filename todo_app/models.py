from django.db import models
from base_user.models import MyUser

choices = (('SSH', ("SSH")),
           ('FTB', ("FTB")),
           ('ADMIN', ("ADMIN")),
           ('EMAIL', ("EMAIL")))


# Create your models here.
class Key(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)

    type = models.CharField(max_length=255, choices=choices)
    host = models.CharField(max_length=12)
    port = models.PositiveIntegerField(null=True, blank=True)
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.type}'
