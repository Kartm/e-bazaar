from django.urls import path
from . import views

app_name = "stats"

urlpatterns = [
    path("stats", views.StatsView.as_view(), name="stats_view"),
]