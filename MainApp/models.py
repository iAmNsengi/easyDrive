from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    HIRED = 'hired'
    AVAILABLE = 'available'
    OFF_DUTY = 'off_duty'
    STATUS_CHOICES = [
        (HIRED, 'Hired'),
        (AVAILABLE, 'Available'),
        (OFF_DUTY, 'Off Duty'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='driver/', null=True, default='avatar.jpg')
    category = models.CharField(max_length=100, null=True)
    bio = models.TextField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_status_display()}'

    class Meta:
        ordering = ['-created_at']

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='company/', null=True, default='avatar.jpg')
    bio = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-created_at']

class Job(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    applicants = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.creator.username} - {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'

    class Meta:
        ordering = ['-created_at']
