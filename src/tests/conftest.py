import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from src.task.models import CategoryModel, TaskModel

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_dono(db):
    return User.objects.create_user(username="jadson", password="123")

@pytest.fixture
def user_outro(db):
    return User.objects.create_user(username="outro_usuario", password="123")

@pytest.fixture
def auth_client_dono(api_client, user_dono):
    api_client.force_authenticate(user=user_dono)
    return api_client

@pytest.fixture
def categoria_dono(user_dono):
    return CategoryModel.objects.create(name="CASA", user=user_dono)

@pytest.fixture
def tarefa_dono(user_dono, categoria_dono):
    return TaskModel.objects.create(
        title="Tarefa",
        description="faça",
        status="PENDENTE",
        priority="ALTA",
        due_date="2026-06-25T00:00:00Z",  # Formato ISO correto para o Django
        user=user_dono,
        category=categoria_dono
    )