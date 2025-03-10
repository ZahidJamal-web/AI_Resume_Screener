from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="uploads/")
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)  # Store AI analysis results as JSON
    score = models.FloatField(null=True, blank=True)  # Store the match score, can be null if not calculated yet

    def __str__(self):
        return f"{self.user.username} - {self.filename}"


class JobDescription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_descriptions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title