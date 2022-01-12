from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("calculate/", views.calculate_view),
    path("correlation", views.correlation_view, name="correlation"),
    path("create_type/", views.create_type, name='create_type'),
    path("delete_type/<int:type_id>", views.delete_type, name='delete_type'),
]
