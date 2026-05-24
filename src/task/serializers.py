from rest_framework import serializers
from src.task.models import CategoryModel, TaskModel
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'name']
class TaskSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    owner = serializers.ReadOnlyField(source='user.username') 
    class Meta:
       model = TaskModel
       fields = ['id', 'title', 'status', 'priority', 'deadline', 'category', 'category_detail', 'owner', 'shared_with']