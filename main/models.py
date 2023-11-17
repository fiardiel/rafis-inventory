from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=255)
    damage = models.IntegerField()
    rarity = models.CharField(max_length=3)