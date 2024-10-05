# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'gyminfo', views.GymInfoViewSet,basename='gyminfo')
router.register(r'createUser',views.CreateUserViewSet)
router.register(r'gymlist',views.GymDetailsforCustomerViewSet,'gymlist')

urlpatterns = [
    path('', include(router.urls)),
    path('my_user/',views.userDetails),
    path('updateUser/',views.updateUserDetails)
]
