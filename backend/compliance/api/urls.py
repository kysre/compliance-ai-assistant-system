from django.urls import path

from compliance.api import views

urlpatterns = [
    path("insert/", views.insert, name="insert"),
    path("batch-insert/", views.batch_insert, name="batch_insert"),
    path("query/", views.query, name="query"),
]
