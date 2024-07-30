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
    experience = models.IntegerField(null=True, blank=True)  
    license_number = models.CharField(max_length=50, null=True, blank=True)
    license_type = models.CharField(max_length=50, null=True, blank=True)
    license_expiration = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    rating = models.FloatField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_status_display()}'

    class Meta:
        ordering = ['-created_at']

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='company/', null=True, default='avatar.jpg')
    name = models.CharField(max_length=255,default="")
    location = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Job(models.Model):
    OPEN = 'open'
    CLOSED = 'closed'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    FULLTIME = 'full-time'
    PARTTIME = 'part-time'
    CONTRACT = 'contract'

    TYPE_CHOICES = [
        (FULLTIME, 'full-time'),
        (PARTTIME, 'part-time'),
        (CONTRACT, 'contract'),

    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="")
    location = models.CharField(max_length=255, default="")
    # salary = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    description = models.TextField()
    requirements = models.TextField(null=True, blank=True)
    applicants = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=FULLTIME)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.creator.username}'

    class Meta:
        ordering = ['-created_at']

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    motivation_letter = models.TextField(default="")

    def __str__(self):
        return f'{self.driver.user.username} - {self.job.title}'

    class Meta:
        ordering = ['-application_date']

class Review(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='reviews')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.driver.user.username} by {self.company.name}'

    class Meta:
        ordering = ['-created_at']
