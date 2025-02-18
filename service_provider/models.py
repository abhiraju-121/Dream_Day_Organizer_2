from django.db import models
from user.models import User
# Create your models here.

class ServiceProvider(models.Model):
    ROLE_CHOICES=[
        ('photo_videography','photo_videography'),
        ('event_planners','event_planners'),
        ('catering','catering'),
        ('bride_groom_service','bride_groom_service'),
        ('decoration','decoration'),
        ('transportation','transportation'),
        ('venue_planners','venue_planners'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='service_provider_profile')
    company_name=models.CharField(max_length=200)
    service_type=models.CharField(max_length=20,choices=ROLE_CHOICES,default='event_planners')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name