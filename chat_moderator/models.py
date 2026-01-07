from django.db import models

# Create your models here.

class SystemPromptConfig(models.Model):
    """Stores the custom system prompt for Groq moderation"""
    name = models.CharField(max_length=100, unique=True, default="groq_moderation_prompt")
    prompt_text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (updated: {self.updated_at})"
    
    class Meta:
        verbose_name = "System Promp6t Configuration"
        verbose_name_plural = "System Prompt Configurations"
