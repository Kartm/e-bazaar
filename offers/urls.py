from django.urls import path
from . import views

app_name = "offers"

urlpatterns = [
    path("", views.OfferFeedView.as_view(), name="offers_feed_view"),
    path("offers/<int:pk>", views.OfferDetailView.as_view(), name="offer_details_view"),
    path("offers/create", views.OfferCreateView.as_view(), name="offer_create_view"),
]