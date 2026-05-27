import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_registro_de_usuario_com_sucesso(api_client):
    url = reverse('register_user')  
    payload = {
        "username": "novo_usuario_teste",
        "email": "teste@email.com",      # 🌟 ADICIONADO: O campo que o seu Django estava exigindo!
        "password": "SenhaSegura@2026",  
        "name": "Novo Usuario"           
    }
    response = api_client.post(url, payload, format='json')
    
    if response.status_code != status.HTTP_201_CREATED:
        print("\n❌ ERRO DO DJANGO SERIALIZER:", response.data)
        
    assert response.status_code == status.HTTP_201_CREATED
    assert "message" in response.data

@pytest.mark.django_db
def test_login_gera_tokens_jwt_corretamente(api_client, user_dono):
    url = reverse('token_obtain_pair')
    payload = {
        "username": "jadson",
        "password": "123"  
    }
    response = api_client.post(url, payload, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data