# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'gyminfo', views.GymInfoViewSet, basename='gyminfo')
router.register(r'createUser', views.CreateUserViewSet)
router.register(r'gymlist', views.GymDetailsforCustomerViewSet, basename='gymlist')
router.register(r'gyms', views.createGymInfoViewSet, basename='gyms')


router.register(r'memberships', views.MembershipViewSet,basename = 'memberships')


router.register(r'customerMemberships', views.customerMembershipViewset,basename = 'customerMemberships')
router.register(r'gymOwnerMemberships', views.gymOwnerMemberShipViewset,basename = 'gymOwnerMemberships')


router.register(r'ownerCreatedmemberships', views.GymOwnerCreatedMembershipViewSet,basename = 'gymOwnerCreatedMemberships') #Main One

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),  # API endpoints
    path('api/my_user/', views.userDetails, name='api-my-user'),
    path('api/updateUser/', views.updateUserDetails, name='api-update-user'),
   


    # Frontend template views
    
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),



    path('gymlist/<int:pk>/', views.gym_detail, name='gym_detail'),  
    path('addGymdetails/', views.add_gym_details, name='add_gym_details'),
    path('edit-gym/<int:gym_id>/', views.edit_gym_details, name='edit_gym_details'),
    path('membership-options/', views.customer_membership_options_view, name='membership-options'),



    path('gym-owner/memberships/', views.gym_owner_memberships_page, name='gym_owner_memberships'),
    path('create-membership/', views.create_membership_view, name='create_membership'),


]
