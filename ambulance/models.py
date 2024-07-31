from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone  # Correct import for timezone

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_volunteer = models.BooleanField('Is volunteer', default=False)
    is_public = models.BooleanField('Is public', default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = CloudinaryField('image')
    biography = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    emergency_contact = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class EmergencyService(models.Model):
    SERVICE_TYPES = [
        ('AMB', 'Ambulance'),
        ('FIRE', 'Firefighter'),
    ]
    
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=4, choices=SERVICE_TYPES)
    image = CloudinaryField('image', null=True)
    description = models.TextField()
    location = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.name}"

class VolunteerOpportunity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateTimeField()
    image = CloudinaryField('image', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="volunteer_opportunities")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(EmergencyService, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='Pending')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.date_time}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    service = models.ForeignKey(EmergencyService, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.rating}"

class VolunteerApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.opportunity.title}"
    







