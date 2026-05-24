from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.task.views import TaskViewSet

# 1. Cria o roteador automático do DRF
router = DefaultRouter()

# 2. Registra a ViewSet (O primeiro argumento define o prefixo da URL)
router.register(r'task', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
