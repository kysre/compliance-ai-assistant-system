from django.urls import path

from chats.api import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("threads/", views.get_threads, name="get_threads"),
    path("threads/<uuid:thread_id>/messages/", views.get_messages, name="get_messages"),
]
