from django.db import models
from django.contrib.auth.models import User  # Import the default User model
from Users.models import CustomUser

class GymInfo(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='gyms')  # Owner of the gym
    owner_name = models.CharField(max_length=200)
    gym_name = models.CharField(max_length=100)
    mobile_phone = models.CharField(max_length=15)
    description = models.TextField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.gym_name
