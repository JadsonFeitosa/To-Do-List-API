import pytest
from django.urls import reverse
from rest_framework import status
from src.task.models import TaskModel

@pytest.mark.django_db
def test_criar_tarefa_vinculada_ao_usuario_logado(auth_client_dono, categoria_dono):
    url = reverse('task-list')
    payload = {
        "title": "Configurar o Pytest",
        "status": "PENDENTE",
        "priority": "ALTA",
        "category": categoria_dono.id
    }
    response = auth_client_dono.post(url, payload, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == "Configurar o Pytest"

@pytest.mark.django_db
def test_bloquear_usuario_deslogado_de_ver_tarefas(api_client):
    url = reverse('task-list')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_de_isolamento_de_dados_usuario_nao_ve_tarefa_alheia(api_client, user_dono, user_outro, categoria_dono):
    tarefa_privada = TaskModel.objects.create(
        title="Plano Secreto",
        status="PENDENTE",
        priority="ALTA",
        user=user_dono,
        category=categoria_dono
    )
    api_client.force_authenticate(user=user_outro)
    
    url = reverse('task-detail', kwargs={'pk': tarefa_privada.id})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND