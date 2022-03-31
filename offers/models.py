from django.db import models

from ebazaar import settings


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
    price = models.DecimalField('date published', decimal_places=2)
    shipping = models.TextField()
    open = models.BooleanField()
    last_bump = models.DateTimeField(auto_now_add=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Image(models.Model):
    base64_dump = models.TextField()
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
