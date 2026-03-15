from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    INTERVIEW_MODE = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    ats_score = models.FloatField(null=True, blank=True)
    interview_mode = models.CharField(max_length=10, choices=INTERVIEW_MODE, blank=True, null=True)
    interview_date = models.DateTimeField(blank=True, null=True)
    interview_link = models.URLField(blank=True, null=True)
    interview_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"