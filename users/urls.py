from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("change-password", views.change_password_request, name="change_password"),
    path("change-contact-info", views.change_contact_info_request, name="change_contact_info"),
    path("users/<int:pk>", views.UserProfileView.as_view(), name="user_view"),
    path("favorites", views.FavoritesView.as_view(), name="favorites_view"),
]