from django.db import models
from django.contrib.auth.models import User


class EmergencyType(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Fire, Medical, Security")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class ResponseTeam(models.Model):
    name = models.CharField(max_length=255,unique=True, help_text="Firestation, Ambulance, Natural Disaster Team")
    team_type = models.CharField(max_length=255,help_text="Fire, Medical, Police")
    available = models.BooleanField(default=True)




class Emergency(models.Model):
    emergency_type = models.ForeignKey(EmergencyType,on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True,null=True)
    assigned_teams = models.ManyToManyField(ResponseTeam,blank=True)

    STATUS_CHOICES = (
        ('reported','Reported'),
        ('dispatched','Dispatched'),
        ('on_seen','On Seen'),
        ('resolved','Resolved'),
        ('cancelled','Cancelled'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='reported')


    def __str__(self):
        return f"{self.emergency_type} for {self.description} ({reported_at})"
    
class EmergencyContacts(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    emergency = models.ForeignKey(Emergency, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
        