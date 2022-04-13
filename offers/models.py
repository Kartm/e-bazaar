from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=200)


class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class District(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=200)


class Subcategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Offer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    shipping = models.TextField()
    open = models.BooleanField(default=True)
    last_bump = models.DateTimeField(default=timezone.now)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    favorites = models.ManyToManyField(
        get_user_model(),
        related_name='favorites',
    )  # TODO: check if each favorite is unique


class Image(models.Model):
    base64_dump = models.TextField()
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
