from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    image = models.URLField(blank=True)
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)