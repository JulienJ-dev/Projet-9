from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        auth_views.LoginView.as_view(
            template_name="authentication/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("compte/", include("authentication.urls")),
]