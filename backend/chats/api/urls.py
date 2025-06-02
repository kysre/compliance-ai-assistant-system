from django.urls import path

from chats.api import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("threads/", views.ThreadView.as_view(), name="threads"),
    path("threads/<uuid:thread_id>/messages/", views.get_messages, name="get_messages"),
]
