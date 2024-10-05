# gymDetails/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import GymInfo, CustomUser
from .serializers import GymInfoSerializer, CreateGymInfoSerializer, CreateUserSerializer
from rest_framework import decorators
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status


class GymInfoViewSet(viewsets.ModelViewSet):
    queryset = GymInfo.objects.all()
    permission_classes = [IsAuthenticated]  # Uncomment this line to require authentication

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CreateGymInfoSerializer  # Use CreateGymInfoSerializer for POST, PUT, PATCH
        return GymInfoSerializer  # Use GymInfoSerializer for other methods



class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    #permission_classes = [AllowAny]  # Allow public access or set to IsAuthenticated as needed

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Method 'GET' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response({"detail": "Method 'GET' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PUT' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PATCH' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Method 'DELETE' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)  # Allow only POST for create
    

@api_view(['GET'])
def userDetails(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # You can choose what user information to return
        user_data = {
           
            'phone_number': request.user.phone_number,
            'email': request.user.email,
            'name':request.user.first_name + ' ' +request.user.last_name
            # Add any other fields you want to include
        }
        return Response(user_data)  # Use Response instead of JsonResponse
    else:
        return Response({'error': 'User not authenticated'}, status=401)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserDetails(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        
        # Update user fields with provided data
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        # Validate phone number uniqueness if provided
        if phone_number:
            # Check if the phone number already exists for another user
            if CustomUser.objects.filter(phone_number=phone_number).exclude(id=user.id).exists():
                return Response({'error': 'This phone number is already associated with another account.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            user.phone_number = phone_number

        # Optionally validate email uniqueness if needed
        if email:
            # Check if the email already exists for another user
            if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({'error': 'This email is already associated with another account.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            user.email = email
        
        # Update other fields if provided
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        
        # Save the user instance
        user.save()

        # Prepare the response data
        updated_user_data = {
            'phone_number': user.phone_number,
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}"
        }
        
        return Response(updated_user_data, status=status.HTTP_200_OK)
    
    return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)