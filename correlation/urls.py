from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("calculate/", views.calculate_view),
    path("correlation", views.correlation_view, name="correlation"),
    path("create_type/<str:name>", views.create_type),
]
