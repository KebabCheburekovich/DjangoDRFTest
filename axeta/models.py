from django.contrib.auth.models import User, AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    name = models.CharField(max_length=255, default="John Smith")
    avatar = models.ImageField(upload_to='avatars/', default='default.png')


class Location(models.Model):
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Skill(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
