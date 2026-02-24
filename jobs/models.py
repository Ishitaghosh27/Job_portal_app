from django.db import models
from django.conf import settings

class Job(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs_posted')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/')
    date_applied = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"
