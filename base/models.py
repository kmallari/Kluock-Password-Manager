from django.db import models
from django.core.validators import MinLengthValidator
from nanoid import generate


class Credentials(models.Model):
    id = models.CharField(
        max_length=21,
        validators=[MinLengthValidator(21)],
        primary_key=True,
        default=generate(),
    )
    website = models.CharField(max_length=256, default="")
    password = models.CharField(max_length=256, default="")
    login = models.CharField(max_length=256, default="")
    created_at = models.DateTimeField(auto_now_add=True)


class Autofill(models.Model):
    website = models.CharField(max_length=256, default="")
    autofill = models.BooleanField(default=True)
