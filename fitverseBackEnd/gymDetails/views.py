# gymDetails/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import GymInfo, CustomUser,Membership,GymOwnerCreatedMembership
from .serializers import GymInfoSerializer, CreateGymInfoSerializer, CreateUserSerializer,GymOwnerCreatedMembershipSerializer
from rest_framework import decorators
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

from . import serializers

from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required



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

class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.customerMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        gym_id = self.request.query_params.get('gym_id')

        # Return memberships for the authenticated user and specific gym if gym_id is provided
        if gym_id:
            return Membership.objects.filter(user=user, gym__id=gym_id)
        return Membership.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        gym_id = request.data.get('gym_id')
        membership_type = request.data.get('membership_type')

        # Ensure the gym exists
        gym = get_object_or_404(GymInfo, id=gym_id)

        # Check if the user already has a membership for this gym
        existing_membership = Membership.objects.filter(user=request.user, gym=gym).first()
        if existing_membership:
            return Response({
                "detail": "You already have a membership for this gym."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create the membership instance
        membership = Membership.objects.create(
            user=request.user,
            gym=gym,
            expiration_date=self.calculate_expiration_date(membership_type),
            membership_type=membership_type
        )

        serializer = self.get_serializer(membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def calculate_expiration_date(self, membership_type):
        from datetime import timedelta, date
        
        if membership_type == 'day':
            return date.today() + timedelta(days=1)
        elif membership_type == 'weekly':
            return date.today() + timedelta(weeks=1)
        elif membership_type == 'monthly':
            return date.today() + timedelta(days=30)
        elif membership_type == 'quarterly':
            return date.today() + timedelta(days=90)
        elif membership_type == 'annually':
            return date.today() + timedelta(days=365)
        else:
            raise ValueError('Invalid membership type')


class customerMembershipViewset(viewsets.ModelViewSet):

    serializer_class = serializers.customerMembershipSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        # Access request.user in this method
        return Membership.objects.filter(user=self.request.user)


class gymOwnerMemberShipViewset(viewsets.ModelViewSet):

    serializer_class = serializers.gymOwnerMembershipSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        # Get all gyms owned by the logged-in gym owner (request.user)
        owner_gyms = GymInfo.objects.filter(owner=self.request.user)
        # Return all memberships associated with those gyms
        return Membership.objects.filter(gym__in=owner_gyms)





from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Membership, GymInfo
from .serializers import GymOwnerCreatedMembershipSerializer
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import GymInfo, GymOwnerCreatedMembership
from .serializers import GymOwnerCreatedMembershipSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import GymInfo, GymOwnerCreatedMembership
from .serializers import GymOwnerCreatedMembershipSerializer


class GymOwnerCreatedMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = GymOwnerCreatedMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get all gyms owned by the logged-in gym owner (request.user)
        owner_gyms = GymInfo.objects.filter(owner=self.request.user)
        return GymOwnerCreatedMembership.objects.filter(gym__in=owner_gyms)

    














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
        # Render the template if the method is POST, but we'll handle API calls in the frontend
        return render(request, 'signup.html') 

    return render(request, 'signup.html')  # Render signup page for GET request
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def gym_detail(request, pk):
    return render(request, 'gym_detail.html', {'gym_id': pk})
# Need to fix this part


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


@login_required
def edit_gym_details(request, gym_id):
    # The actual editing is handled via API; this view renders the edit page
    gym = get_object_or_404(GymInfo, id=gym_id, owner=request.user)
    context = {
        'gym_id': gym.id,
    }
    return render(request, 'edit_gym_details.html', context)


@login_required
def customer_membership_options_view(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    # Optionally, you can pass any context you need to the template
    return render(request, 'membership_options.html')

@login_required
def gym_owner_memberships_page(request):
    return render(request, 'gym_owner_memberships.html')