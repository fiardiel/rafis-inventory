from django.db import models

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=255)
    damage = models.IntegerField()