from django.urls import path

from . import views

urlpatterns = [
    path("api/insert/", views.insert, name="insert"),
    path("api/batch-insert/", views.batch_insert, name="batch_insert"),
    path("api/query/", views.query, name="query"),
]
