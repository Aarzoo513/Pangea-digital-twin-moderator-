from django.urls import path
from . import views

urlpatterns = [
    path("", views.moderate, name="moderate"),
    path("api/ask/", views.api_ask, name="api_ask"),  # 👈 new JSON endpoint
    path("api/prompt/get/", views.api_get_prompt, name="api_get_prompt"),
    path("api/prompt/update/", views.api_update_prompt, name="api_update_prompt"),
    path("api/prompt/reset/", views.api_reset_prompt, name="api_reset_prompt"),
]


