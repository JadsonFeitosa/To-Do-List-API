import django.urls
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from src.task.models import TaskModel
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
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_completed', 'category','status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date']
    http_method_names = ['get', 'post']

    def get_queryset(self):
        # Garante que o usuário só veja suas tarefas ou as compartilhadas com ele
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