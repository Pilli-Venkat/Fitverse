from rest_framework import serializers
from .models import GymInfo, CustomUser, Membership, GymOwnerCreatedMembership
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'email', 'first_name', 'last_name']  # Add any other fields you want to include

class GymInfoSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='gymlist-detail')
    
    class Meta:
        model = GymInfo
        fields = ['id', 'gym_name', 'description', 'city', 'owner', 'url']

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

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user_type', 'phone_number', 'email', 'first_name', 'last_name', 'password']  # Add any other fields you want to include
    
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class CustomerMembershipSerializer(serializers.ModelSerializer):
    days_until_expiration = serializers.ReadOnlyField() 
    gym = GymInfoSerializer()

    class Meta:
        model = Membership
        fields = ['id', 'user', 'gym', 'start_date', 'expiration_date', 'membership_type', 'days_until_expiration']

class GymOwnerMembershipSerializer(serializers.ModelSerializer):
    days_until_expiration = serializers.ReadOnlyField() 
    user = CustomUserSerializer()

    class Meta:
        model = Membership
        fields = ['id', 'user', 'gym', 'start_date', 'expiration_date', 'membership_type', 'days_until_expiration']

class GymOwnerCreatedMembershipSerializer(serializers.ModelSerializer):
    days_until_expiration = serializers.ReadOnlyField()
    membership_status = serializers.SerializerMethodField()
    gym = serializers.PrimaryKeyRelatedField(queryset=GymInfo.objects.none())
    expiration_date = serializers.ReadOnlyField()

    class Meta:
        model = GymOwnerCreatedMembership
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 
            'address', 'gym', 'start_date', 'membership_type', 
            'membership_option', 'days_until_expiration', 
            'membership_status', 'expiration_date', 'deleted'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['gym'].queryset = GymInfo.objects.filter(owner=request.user)
   
    def get_membership_status(self, obj):
        today = timezone.now().date()
        if obj.start_date <= today <= obj.expiration_date:
            return "active"
        elif today < obj.start_date:
            return "upcoming"
        else:
            return "expired"

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if user.user_type != 'gym_owner':
            raise ValidationError("You are not allowed to add memberships.")

        existing_membership = GymOwnerCreatedMembership.objects.filter(
            phone_number=validated_data['phone_number'], 
            gym=validated_data['gym']
        )

        today = timezone.now().date()
        # Filter existing memberships that are either active or upcoming
        active_or_upcoming = existing_membership.filter(
            start_date__lte=today,
            expiration_date__gte=today
        ).exists() or existing_membership.filter(
            start_date__gt=today
        ).exists()
        if active_or_upcoming:
            raise ValidationError({"phone_number": f"A membership with this phone number is Active/ Upcoming Plan."})

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
        instance.membership_option = validated_data.get('membership_option', instance.membership_option)
        # Recalculate expiration date only if membership_type or start_date has changed
        if 'membership_type' in validated_data or 'start_date' in validated_data:
            instance.expiration_date = self.calculate_expiration_date(
                instance.membership_type, instance.start_date
            )

        # Save the updated instance
        instance.save()
        return instance

    def calculate_expiration_date(self, membership_type, start_date):
        membership_durations = {
            'day': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'half_month': timedelta(days=15),
            'monthly': timedelta(weeks=4),
            'quarterly': timedelta(weeks=12),
            'annually': timedelta(weeks=52),
        }

        try:
            return start_date + membership_durations[membership_type]
        except KeyError:
            raise ValidationError("Invalid membership type")
