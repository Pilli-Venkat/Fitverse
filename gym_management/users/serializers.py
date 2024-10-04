# users/serializers.py

from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'email', 'name', 'role', 'password', 'token')

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid phone number or password')

            if not user.check_password(password):
                raise serializers.ValidationError('Invalid phone number or password')

        else:
            raise serializers.ValidationError('Must provide phone number and password')

        data['user'] = user
        return data


# users/serializers.py
# current user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'email', 'name', 'role')
