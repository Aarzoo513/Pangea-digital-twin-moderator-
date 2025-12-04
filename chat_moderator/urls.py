from django.urls import path
from . import views

urlpatterns = [
    path("", views.moderate, name="moderate"),
    path("api/ask/", views.api_ask, name="api_ask"),  # 👈 new JSON endpoint
]
