from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.country}, {self.name}"


class District(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city}, {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category}: {self.name}"


class OfferManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(open=True)


class Offer(models.Model):
    active_offer_objects = OfferManager()

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
    )

    class Meta:
        ordering = ['-last_bump']


class Image(models.Model):
    base64_dump = models.TextField()
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
