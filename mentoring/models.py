from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import CustomUser
            

class MentorshipSession(models.Model):
    requesting_user = models.ForeignKey(CustomUser, related_name='requesting_user', on_delete=models.CASCADE)
    mentor = models.ForeignKey(CustomUser, related_name='mentor_sessions', on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    scheduled_time = models.TextField()
    is_accepted = models.BooleanField(null=True, default=None)
