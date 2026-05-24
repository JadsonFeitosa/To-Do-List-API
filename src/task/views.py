import django.contrib.auth.models
import django.urls
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from src.task.models import CategoryModel, TaskModel
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskViewSet(viewsets.ModelViewSet):
    queryset = TaskModel.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_completed', 'category','status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date']
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_queryset(self):
        user = self.request.user
        return TaskModel.objects.filter(Q(user=user) | Q(shared_with=user)).distinct()

    def list(self, request: Request, *args: any, **kwargs: any) -> Response:
        queryset = self.get_queryset()
        
        serializer = self.get_serializer(queryset, many=True)
        
        resposta_customizada = {
            "total": len(serializer.data),
            "status": "sucesso",
            "dados": serializer.data
        }
        
        return Response(data=resposta_customizada, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        data = {
            "pending": queryset.filter(status='PENDING').count(),
            "in_progress": queryset.filter(status='IN_PROGRESS').count(),
            "completed": queryset.filter(status='COMPLETED').count(),
        }
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='share-task')
    def share_task(self, request, pk=None):
        task = self.get_object()

        shared_user = request.data.get('id_user', None)
        
        if task.owner != request.user:
            return Response(
                {"error": "Você só pode compartilhar tarefas das quais é o dono."},
                status=status.HTTP_400_BAD_REQUEST
                
            )
        
        if shared_user == None:
            return Response(
                {"error": "Usuario é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_to_share = User.objects.get(id=shared_user)

        if user_to_share == None:
                return Response(
                    {"error": "Usuario inexistente."},
                    status=status.HTTP_400_BAD_REQUEST
        )
            

        if user_to_share == request.user:
            return Response(
                {"error": "Você não pode compartilhar uma tarefa com você mesmo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Adiciona o usuário à relação ManyToMany
        task.shared_with.add(user_to_share)
        return Response(
            {"message": f"Tarefa compartilhada com sucesso com '{user_to_share.username}'."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='is-completed')
    def conpleted_task(self, request, pk=None):
        task = self.get_object()
        task.is_completed = True
        task.save()
        return Response(
            {"message": f"Tarefa concluida com sucesso"},
            status=status.HTTP_200_OK
        )
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_queryset(self):
        user = self.request.user
        return CategoryModel.objects.filter(user=user).distinct()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)