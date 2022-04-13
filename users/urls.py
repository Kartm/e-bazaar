from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("users/<int:pk>", views.user_view, name="user_view"),
]