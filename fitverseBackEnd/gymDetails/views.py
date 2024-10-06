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

    permission_classes = [IsAuthenticated]  # Require authentication
    def get_queryset(self):
        # Access request.user in this method
        return GymInfo.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CreateGymInfoSerializer  # Use CreateGymInfoSerializer for POST, PUT, PATCH
        return GymInfoSerializer  # Use GymInfoSerializer for other methods
    

class createGymInfoViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]  # Require authentication
    serializer_class = CreateGymInfoSerializer
    def get_queryset(self):
        # Access request.user in this method
        return GymInfo.objects.filter(owner=self.request.user)
    


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
            'name':request.user.first_name + ' ' +request.user.last_name,
            'account_type': request.user.user_type
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



class GymDetailsforCustomerViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]  # Uncomment if you want authentication

    queryset = GymInfo.objects.all()
    serializer_class = GymInfoSerializer







# FRONT END VIEWS

    # views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Home page view
def home_view(request):
    return render(request, 'home.html')

# Login view
def login_view(request):
    print("LOGIN VIEW CALLED")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

import requests
from django.shortcuts import render, redirect
# Signup view
# gymDetails/views.py
import requests
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password1']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_type = request.POST['user_type']

        user_data = {
            'user_type': user_type,
            'phone_number': phone_number,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }

        # Make a request to the signup API
        response = requests.post('http://127.0.0.1:8000/api/createUser/', json=user_data)

        # Print status code and content for debugging
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.content)

        if response.status_code == 201:
            return redirect('login')
        else:
            # Handle API error response
            return render(request, 'signup.html', {'error': response.text})  # Use response.text for raw content

    return render(request, 'signup.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, get_object_or_404

def gym_detail(request, pk):  # Ensure it accepts pk
    gym = get_object_or_404(Gym, pk=pk)  # Use pk to get the Gym object
    return render(request, 'gym_detail.html', {'gym': gym})

# Need to fix this part
  
from django.shortcuts import render, redirect
from .models import GymInfo
from django.contrib.auth.decorators import login_required

@login_required
def add_gym_details(request):
    if request.method == 'POST':
        # Get form data
        gym_name = request.POST.get('gym_name')
        description = request.POST.get('description')
        city = request.POST.get('city')

        # Save the gym details
        GymInfo.objects.create(owner=request.user, gym_name=gym_name, description=description, city=city)

        # Redirect to a success page or home
        return redirect('home')  # Assuming 'home' is a defined URL name

    return render(request, 'add_gym_details.html')
