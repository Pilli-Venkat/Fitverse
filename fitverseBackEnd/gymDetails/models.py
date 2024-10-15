from django.db import models
from Users.models import CustomUser
from django.utils import timezone

class GymInfo(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='gyms')  # Owner of the gym
    gym_name = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.gym_name


class Membership(models.Model):
    MEMBERSHIP_TYPE_CHOICES = [
        ('day', 'Day'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='memberships')
    gym = models.ForeignKey(GymInfo, on_delete=models.CASCADE, related_name='memberships')
    start_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPE_CHOICES)

    def __str__(self):
        return f'{self.user.first_name} - {self.gym.gym_name} ({self.get_membership_type_display()})'

    @property
    def days_until_expiration(self):
        today = timezone.now().date()

        # Case 1: Plan has not started yet
        if self.start_date > today:
            days_until_start = (self.start_date - today).days
            return f"Start in {days_until_start} days"

        # Case 2: Plan has started, but not expired
        elif self.start_date <= today <= self.expiration_date:
            days_until_expiration = (self.expiration_date - today).days
            return f"Expire in {days_until_expiration} days"

        # Case 3: Plan has expired
        else:
            return "Plan has expired"

class GymOwnerCreatedMembership(models.Model):
    MEMBERSHIP_TYPE_CHOICES = [
        ('day', 'Day'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    gym = models.ForeignKey(GymInfo, on_delete=models.CASCADE, related_name='memberships_created_by_owners')
    start_date = models.DateField()
    expiration_date = models.DateField()
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPE_CHOICES)
    #created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.gym.gym_name} ({self.get_membership_type_display()})'

    @property
    def days_until_expiration(self):
        today = timezone.now().date()

        if self.start_date > today:
            days_until_start = (self.start_date - today).days
            return f"Starts in {days_until_start} days"
        elif self.start_date <= today <= self.expiration_date:
            days_until_expiration = (self.expiration_date - today).days
            return f"Expires in {days_until_expiration} days"
        else:
            days_since_expiration = (today - self.expiration_date).days
            if days_since_expiration < 5:
                return f"Expired before {days_since_expiration} days"
            else:
                return "Expired"


    @property
    def membership_status(self):
        today = timezone.now().date()
        if self.start_date > today:
            return "Upcoming"
        elif self.start_date <= today <= self.expiration_date:
            return "Active"
        else:
            return "Expired"
