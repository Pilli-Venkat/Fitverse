from rest_framework import serializers
from .models import GymInfo, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'email', 'first_name', 'last_name']  # Add any other fields you want to include

class GymInfoSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer()

    class Meta:
        model = GymInfo
        fields = ['id', 'gym_name', 'mobile_phone', 'description', 'city', 'owner']

class CreateGymInfoSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)  # Set as read-only

    class Meta:
        model = GymInfo
        fields = ['id', 'gym_name', 'mobile_phone', 'description', 'city', 'owner']

    def create(self, validated_data):
        request = self.context.get('request')  # Get the request from context
        user = request.user  # Get the current user
        validated_data['owner'] = user  # Set the owner to the current user
        return super().create(validated_data)

# To create or register User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'email', 'first_name', 'last_name','password']  # Add any other fields you want to include
    
    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
