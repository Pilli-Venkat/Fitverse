from rest_framework import serializers
from .models import GymInfo, CustomUser,GymOwnerCreatedMembership
from rest_framework.exceptions import ValidationError  
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'email', 'first_name', 'last_name']  # Add any other fields you want to include

class GymInfoSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='gymlist-detail')
    class Meta:
        model = GymInfo
        fields = ['id', 'gym_name', 'description', 'city', 'owner','url']

class CreateGymInfoSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only

    class Meta:
        model = GymInfo
        fields = ['id', 'gym_name', 'description', 'city', 'owner']

    def create(self, validated_data):
        request = self.context.get('request')  # Get the request from context
        user = request.user  # Get the current user
        
        # Check if the user is of type 'gym_owner'
        if user.user_type != 'gym_owner':
            raise ValidationError("You are not allowed to add GymInfo because you are not a gym owner.")
        
        validated_data['owner'] = user  # Set the owner to the current user
        return super().create(validated_data)
    

# To create or register User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user_type','phone_number', 'email', 'first_name', 'last_name','password']  # Add any other fields you want to include
    
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


from rest_framework import serializers
from .models import Membership

class customerMembershipSerializer(serializers.ModelSerializer):
    days_until_expiration = serializers.ReadOnlyField() 
    gym = GymInfoSerializer()
    class Meta:
        model = Membership
        fields = ['id', 'user', 'gym', 'start_date', 'expiration_date', 'membership_type','days_until_expiration']

class gymOwnerMembershipSerializer(serializers.ModelSerializer):
    days_until_expiration = serializers.ReadOnlyField() 
    user = CustomUserSerializer()
    class Meta:
        model = Membership
        fields = ['id', 'user', 'gym', 'start_date', 'expiration_date', 'membership_type','days_until_expiration']
from rest_framework import serializers
from .models import GymOwnerCreatedMembership, GymInfo
from django.utils import timezone
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import GymOwnerCreatedMembership, GymInfo  # Adjust import based on your project structure

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import GymOwnerCreatedMembership, GymInfo  # Adjust import based on your project structure
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import GymOwnerCreatedMembership, GymInfo  # Adjust import based on your project structure
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import GymOwnerCreatedMembership, GymInfo  # Adjust import based on your project structure
from datetime import timedelta

class GymOwnerCreatedMembershipSerializer(serializers.ModelSerializer):
    days_until_expiration = serializers.ReadOnlyField()
    membership_status = serializers.ReadOnlyField()  # New field for status
    gym = serializers.PrimaryKeyRelatedField(queryset=GymInfo.objects.none())
    expiration_date = serializers.ReadOnlyField()  # Make expiration_date read-only
    class Meta:
        model = GymOwnerCreatedMembership
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 
            'address', 'gym', 'start_date', 'membership_type', 
            'days_until_expiration', 'membership_status','expiration_date'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Filtering gyms based on the logged-in user (who is the gym owner)
            self.fields['gym'].queryset = GymInfo.objects.filter(owner=request.user)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # Ensuring only gym owners can add memberships
        if user.user_type != 'gym_owner':
            raise ValidationError("You are not allowed to add GymInfo because you are not a gym owner.")

        # Check for an existing membership with the same phone number
        existing_membership = GymOwnerCreatedMembership.objects.filter(
            phone_number=validated_data['phone_number'],
            gym=validated_data['gym']
        )

        # Get today's date
        today = timezone.now().date()

        # Check if there's an active or upcoming membership
        active_or_upcoming = existing_membership.filter(
            start_date__lte=today,
            expiration_date__gte=today
        ).exists()

        if active_or_upcoming:
            raise ValidationError(f"Membership is already active for this phone number- {validated_data['phone_number']}")

        # Check for memberships that start in the future
        upcoming_membership = existing_membership.filter(
            start_date__gt=today
        ).exists()

        if upcoming_membership:
            raise ValidationError("Membership starts in the future for this phone number.")

        # Calculate the expiration date based on membership type and start date
        validated_data['expiration_date'] = self.calculate_expiration_date(
            validated_data['membership_type'], validated_data['start_date']
        )

        return super().create(validated_data)
    def update(self, instance, validated_data):
        # Update the instance with validated data
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.membership_type = validated_data.get('membership_type', instance.membership_type)
        
        # Calculate new expiration date
        instance.expiration_date = self.calculate_expiration_date(
            instance.membership_type, instance.start_date
        )


        # Save the updated instance
        instance.save()
        return instance

    def calculate_expiration_date(self, membership_type, start_date):
        membership_durations = {
            'day': timedelta(days=0),
            'weekly': timedelta(weeks=1),
            'monthly': timedelta(weeks=4),
            'quarterly': timedelta(weeks=12),
            'annually': timedelta(weeks=52),
        }

        try:
            return start_date + membership_durations[membership_type]
        except KeyError:
            raise ValueError("Invalid membership type")
