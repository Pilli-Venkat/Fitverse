# gymDetails/views.py

# ==========================
# BACKEND IMPORTS
# ==========================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import GymInfo, CustomUser, Membership, GymOwnerCreatedMembership
from .serializers import (GymInfoSerializer, CreateGymInfoSerializer,
                          CreateUserSerializer, GymOwnerCreatedMembershipSerializer,CustomerMembershipSerializer)

# ==========================
# BACKEND VIEWS
# ==========================
class GymInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GymInfo.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CreateGymInfoSerializer
        return GymInfoSerializer




class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer

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
        return super().create(request, *args, **kwargs)


@api_view(['GET'])
def userDetails(request):
    if request.user.is_authenticated:
        user_data = {
            'phone_number': request.user.phone_number,
            'email': request.user.email,
            'name': f"{request.user.first_name} {request.user.last_name}",
            'account_type': request.user.user_type
        }
        return Response(user_data)
    return Response({'error': 'User not authenticated'}, status=401)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserDetails(request):
    if request.user.is_authenticated:
        user = request.user
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if phone_number and CustomUser.objects.filter(phone_number=phone_number).exclude(id=user.id).exists():
            return Response({'error': 'This phone number is already associated with another account.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if phone_number:
            user.phone_number = phone_number
        if email and CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            return Response({'error': 'This email is already associated with another account.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()

        updated_user_data = {
            'phone_number': user.phone_number,
            'email': user.email,
            'name': f"{user.first_name} {user.last_name}"
        }

        return Response(updated_user_data, status=status.HTTP_200_OK)

    return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class GymDetailsforCustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GymInfo.objects.all()
    serializer_class = GymInfoSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class =CustomerMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        gym_id = self.request.query_params.get('gym_id')

        if gym_id:
            return Membership.objects.filter(user=user, gym__id=gym_id)
        return Membership.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        gym_id = request.data.get('gym_id')
        membership_type = request.data.get('membership_type')

        gym = get_object_or_404(GymInfo, id=gym_id)

        if Membership.objects.filter(user=request.user, gym=gym).exists():
            return Response({"detail": "You already have a membership for this gym."},
                            status=status.HTTP_400_BAD_REQUEST)

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

        expiration_map = {
            'day': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'monthly': timedelta(days=30),
            'quarterly': timedelta(days=90),
            'annually': timedelta(days=365),
        }

        if membership_type not in expiration_map:
            raise ValueError('Invalid membership type')
        
        return date.today() + expiration_map[membership_type]






class GymOwnerCreatedMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = GymOwnerCreatedMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        owner_gyms = GymInfo.objects.filter(owner=self.request.user)
        return GymOwnerCreatedMembership.objects.filter(gym__in=owner_gyms, deleted=False)

    @action(detail=False, methods=['get'], url_path='check_phone/(?P<phone_number>[^/.]+)')
    def check_phone(self, request, phone_number=None):
        gym_ids = GymInfo.objects.filter(owner=request.user).values_list('id', flat=True)
        memberships = GymOwnerCreatedMembership.objects.filter(phone_number=phone_number, gym__in=gym_ids).order_by('-start_date')

        if memberships.exists():
            membership = memberships.first()
            serializer = self.get_serializer(membership)
            return Response({"exists": True, **serializer.data}, status=status.HTTP_200_OK)
        return Response({"exists": False}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        membership = self.get_object()
        if membership.membership_status in ['Upcoming', 'Active']:
            raise ValidationError(f"You cannot delete an {membership.membership_status} membership.")

        membership.deleted = True
        membership.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================
# FRONTEND IMPORTS
# ==========================
import requests

# ==========================
# FRONTEND VIEWS
# ==========================
def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        return render(request, 'signup.html')  # Handle API calls in the frontend
    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def gym_detail(request, pk):
    return render(request, 'gym_detail.html', {'gym_id': pk})


@login_required
def edit_gym_details(request, gym_id):
    gym = get_object_or_404(GymInfo, id=gym_id, owner=request.user)
    context = {
        'gym_id': gym.id,
    }
    return render(request, 'edit_gym_details.html', context)


@login_required
def customer_membership_options_view(request):
    return render(request, 'membership_options.html')


@login_required
def gym_owner_memberships_page(request):
    return render(request, 'gym_owner_memberships.html')


def create_membership_view(request):
    return render(request, 'create_membership.html')
