from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobApplication
from .utils import calculate_match_score

@receiver(post_save, sender=JobApplication)
def calculate_application_match_score(sender, instance, created, **kwargs):
    """
    Auto-calculate AI match score when application is created
    """
    if created and not instance.ai_match_score:
        match_score = calculate_match_score(instance.student, instance.job)
        instance.ai_match_score = match_score
        instance.save(update_fields=['ai_match_score'])
