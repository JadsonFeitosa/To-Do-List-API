from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.task.views import TaskViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from src.user.views import RegisterView

router = DefaultRouter()

router.register(r'task', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'), 

    path('register-user/', RegisterView.as_view(), name='register_user'),
]
