from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager


# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    profile_image=models.ImageField(upload_to="images/", null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    @property
    def image_abs(self):
        return self.profile_image.url
    def __str__(self):
        return self.email
