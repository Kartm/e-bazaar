from django.urls import path
from . import views

app_name = "offers"

urlpatterns = [
    path("", views.offers_feed_view, name="offers_feed_view"),
    path("offers/<int:pk>", views.offer_details_view, name="offer_details_view"),
]