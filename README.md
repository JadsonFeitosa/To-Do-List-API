# To-Do-List-API
# Advanced To-Do List API (Python)  Esta é uma API RESTful para gerenciamento de listas de tarefas (To-Do List), desenvolvido com foco em alta performance, escalabilidade e manutenibilidade. O projeto conta com autenticação JWT (JSON Web Tokens), documentação interativa automatizada, isolamento de dados por usuário e conteinerização completa utilizando **Docker**.

### 🚀 Como Rodar o Projeto com Docker

  Certifique-se de ter o **Docker** e o **Docker Compose** instalados em sua máquina.
  
    # 1. Clonar o Repositório
    
    # 2. Construir e Subir os Contêineres
    
        Terminal: docker compose up --build
        
    # 3. Executar as Migrações do Banco de Dados
    
        Terminal: docker compose exec api python manage.py migrate
        
        A API estará disponível em: http://127.0.0.1:8000/
        
    # 4. Criar um Usuário para Testes
    
        Terminal: docker compose exec api python manage.py createsuperuser
        
          Sentirá o terminal pedir:
          
            Username: (ex: admin)
            
            E-mail: (pode deixar em branco e dar Enter)
            
            Password: (sua senha - ela não aparece enquanto você digita por segurança)
            
            Password (again): (confirme a senha)
            
    

### 🔑 Como Testar os Endpoints pelo Swagger

  Como a maioria das rotas exige autenticação, siga estes passos para testar tudo direto pela interface do Swagger:
  
    1. Acesse a rota de documentação: `http://127.0.0.1:8000/api/schema/swagger-ui/`.
    2. Localize o endpoint **`POST /token/`**, clique em **"Try it out"**, insira suas credenciais e clique em **"Execute"**.
    3. Copie o valor do token gerado no campo **`access`** (aquela string longa que começa com `eyJ`).
    4. Role a página até o topo, clique no botão **"Authorize"** (ícone de cadeado).
    5. No campo *Value*, cole o token copiado (sem digitar a palavra "Bearer") e clique em **Authorize**.

Pronto! Os cadeados serão ativados e você poderá realizar requisições para todas as rotas protegidas diretamente pelo navegador.
    
Tabela de Endpoints da API
  Todas as rotas (exceto registro, login e documentação) exigem o cabeçalho HTTP Authorization: Bearer <seu_token_jwt>.

  | Módulo | Método | Endpoint | Proteção | Descrição / Parâmetros |
  | :--- | :---: | :--- | :---: | :--- |
  | **Autenticação** | `POST` | `/register-user/` | 🔓 Público | Cria uma nova conta de usuário. |
  | | `POST` | `/token/` | 🔓 Público | Login. Gera os tokens JWT (`access` e `refresh`). |
  | | `POST` | `/refresh-token/` | 🔓 Público | Renova o token `access` usando o `refresh`. |
  | **Categorias** | `GET` | `/categories/` | 🔒 Autenticado | Lista as categorias criadas pelo usuário logado. |
  | | `POST` | `/categories/` | 🔒 Autenticado | Cria uma nova categoria para o usuário logado. |
  | | `PUT` / `PATCH` | `/categories/{id}/` | 🔒 Autenticado | Atualiza ou modifica uma categoria existente por ID. |
  | **Tarefas** | `GET` | `/tasks/` | 🔒 Autenticado | Lista tarefas do usuário + compartilhadas. Filtros: `?status=`, `?priority=`, `?search=` |
  | | `POST` | `/tasks/` | 🔒 Autenticado | Cria uma nova tarefa para o usuário logado. |
  | | `PUT` / `PATCH` | `/tasks/{id}/` | 🔒 Autenticado | Atualiza os dados de uma tarefa (Dono ou compartilhado). |
  | | `GET` | `/tasks/statistics/` | 🔒 Autenticado | Retorna métricas e o total de tarefas por status. |
  | | `POST` | `/tasks/{id}/share-task/` | 🔒 Autenticado | Compartilha a tarefa informando o `id_user` no body. |
  | | `POST` | `/tasks/{id}/is-completed/` | 🔒 Autenticado | Atalho rápido para concluir a tarefa (`is_completed = true`). |
  | **Documentação**| `GET` | `/api/schema/swagger-ui/`| 🔓 Público | Interface interativa do Swagger UI para testar a API. |


Decisões de Design

  O projeto foi desenhado focado em organização, simplicidade e reaproveitamento de código através de três pilares:
  
    SOLID
    
      Responsabilidade Única (SRP): Separação de papéis (SRP): Banco (models), validação (serializers) e rotas HTTP (views).
      
      Extensível (OCP & LSP): Uso do decorador @action para injetar novos endpoints especializados(como compartilhar tarefas) sem quebrar as regras originais do framework.
    
    DRY (Sem repetição)
    
      Automação: Uso de ModelViewSet para gerar todas as rotas de CRUD automaticamente, evitando códigos manuais repetitivos.
      
      Fonte Única: Toda e qualquer validação de dados fica concentrada nos Serializers.
    
    KISS (Código simples)
    
      Filtros Prontos: Uso do DjangoFilterBackend para buscas na URL, eliminando dezenas de linhas de if/else.
      
      Tradução de Campos: Uso do parâmetro source no Serializer para adaptar os nomes dos campos para o front-end de forma rápida e sem mexer no banco.



Segurança e Isolamento de Dados

  A API implementa o Princípio do Menor Privilégio. Através da customização do método get_queryset() nas ViewSets, garantimos que:

    Um usuário autenticado nunca tenha visibilidade ou permissão de alteração sobre as categorias criadas por terceiros.
    
    Um usuário consiga listar e gerenciar exclusivamente as tarefas das quais é o dono oficial ou que foram expressamente compartilhadas com ele através da relação Many-to-Many shared_with.

Tecnologias Utilizadas

  Python 3.14 / Django 6.0
  
  Django REST Framework (DRF)
  
  Docker & Docker Compose (Ambiente isolado e reprodutível)
  
  Simple JWT (Autenticação baseada em tokens)
  
  drf-spectacular (Documentação OpenAPI 3.0 / Swagger)
  
  MySQL 8.1 (Banco de dados relacional oficial)

