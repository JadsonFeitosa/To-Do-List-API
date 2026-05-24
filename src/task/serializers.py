from rest_framework import serializers
from src.task.models import CategoryModel, TaskModel

class TaskSerializer(serializers.ModelSerializer): 
    class Meta:
       model = TaskModel
       fields = ['all']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['all']
