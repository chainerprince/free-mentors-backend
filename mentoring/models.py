from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import CustomUser
            

class MentorshipSession(models.Model):
    mentee = models.ForeignKey(CustomUser, related_name='mentee', on_delete=models.CASCADE)
    mentorId = models.ForeignKey(CustomUser, related_name='mentor_sessions', on_delete=models.CASCADE)
    questions = models.TextField()
    scheduled_time = models.TextField()
    session_accepted = models.BooleanField(null=True, default=None)
