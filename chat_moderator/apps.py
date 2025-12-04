from django.apps import AppConfig
from db.init_db import init_database

class ChatModeratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat_moderator"

    def ready(self):
        # Initialize DB when Django starts
        init_database()