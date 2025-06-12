from django.urls import path

from compliance.api import views

urlpatterns = [
    path("insert/", views.insert, name="insert"),
    path("batch-insert/", views.batch_insert, name="batch_insert"),
    path("query/", views.query, name="query"),
    path("regulations/", views.RegulationListView.as_view(), name="regulations"),
    path(
        "regulations/<str:identifier>/",
        views.RegulationView.as_view(),
        name="regulation",
    ),
]
