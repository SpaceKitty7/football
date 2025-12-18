from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model for GridIron AI"""
    email = models.EmailField(unique=True)
    favorite_team = models.CharField(max_length=50, blank=True, null=True)
    theme_preference = models.CharField(max_length=50, default='default')
    dark_mode = models.BooleanField(default=True)

    # AI Assistant preferences
    ai_risk_tolerance = models.CharField(
        max_length=20,
        choices=[
            ('conservative', 'Conservative'),
            ('balanced', 'Balanced'),
            ('aggressive', 'Aggressive'),
        ],
        default='balanced'
    )
    ai_prioritize_matchups = models.BooleanField(default=True)
    ai_consider_injuries = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
