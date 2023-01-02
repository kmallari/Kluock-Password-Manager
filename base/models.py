from django.db import models
from django.core.validators import MinLengthValidator
from django_cryptography.fields import encrypt
from django.forms import URLField, ValidationError


def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except:
        raise ValidationError((f"{url} is not a valid url"), params={"url": url})
    return True


class Credentials(models.Model):
    id = models.CharField(
        max_length=8,
        validators=[MinLengthValidator(8)],
        primary_key=True,
    )
    website = models.CharField(max_length=256, validators=[validate_url])
    password = encrypt(models.CharField(max_length=256))
    login = models.CharField(max_length=256)
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField(default=0)
    autofill = models.BooleanField(default=True)
