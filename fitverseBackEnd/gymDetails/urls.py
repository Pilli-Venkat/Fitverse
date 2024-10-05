# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'gyminfo', views.GymInfoViewSet)
router.register(r'createUser',views.CreateUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/',views.userDetails),
    path('updateUser/',views.updateUserDetails)
]
