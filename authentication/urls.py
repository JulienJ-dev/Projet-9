from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("inscription/", views.signup, name="signup"),
    path("accueil/", views.home, name="home"),
    path(
        "deconnexion/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]