from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EmergencyType(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Fire, Medical, Security")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class ResponseTeam(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Firestation, Ambulance, Natural Disaster Team")
    team_type = models.CharField(max_length=255, help_text="Fire, Medical, Police")
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Emergency(models.Model):
    # Define location choices
    LOCATION_CHOICES = (
        ('location_1', 'Thika Town'),
        ('location_2', 'Bidco'),
        ('location_3', 'Runda'),
        ('location_4', 'Starehe'),
        ('location_5', 'MKU'),
        ('location_6', 'Thika Level 5'),
        ('location_7', 'Kiandutu'),
        ('location_8', 'Biafra'),
    )

    STATUS_CHOICES = (
        ('reported', 'Reported'),
        ('dispatched', 'Dispatched'),
        ('on_seen', 'On Seen'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    )

    emergency_type = models.ForeignKey(EmergencyType, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    assigned_teams = models.ManyToManyField(ResponseTeam, blank=True)

    # Change location to a CharField with predefined choices
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='location_1', help_text="Select the location of the emergency")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')

    class Meta:
        ordering = ['-reported_at']
        verbose_name = 'Emergency Report'
        verbose_name_plural = 'Emergency Reports'

    def __str__(self):
        return f"{self.emergency_type} for {self.description} (Reported at: {self.reported_at})"

    def mark_as_resolved(self):
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.save()


class EmergencyContacts(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    emergency_type = models.ForeignKey(EmergencyType, on_delete=models.CASCADE)  # Changed field name

    def __str__(self):
        return f"{self.name}"


class PersonalEmergencyContacts(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


class AidTip(models.Model):
    emergency_type = models.CharField(max_length=50)  # e.g., 'Fire', 'Medical', etc.
    tip = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emergency_type}: {self.tip[:50]}"  # Display first 50 characters of the tip
