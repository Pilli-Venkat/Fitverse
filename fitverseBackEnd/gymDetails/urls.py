# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'gyminfo', views.GymInfoViewSet, basename='gyminfo')
router.register(r'createUser', views.CreateUserViewSet)
router.register(r'gymlist', views.GymDetailsforCustomerViewSet, basename='gymlist')
router.register(r'addGymDetails', views.createGymInfoViewSet, basename='addGymDetails'),

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
    path('gymlist/<int:pk>/', views.gym_detail, name='gym_detail'),  # This URL pattern s
    path('addGymdetails/', views.add_gym_details, name='add_gym_details'),
]
