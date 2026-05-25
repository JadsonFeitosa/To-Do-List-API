from django.db import models
from django.contrib.auth.models import User
from src.task.choices import PriorityOptions, StatusTask

class CategoryModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', db_column='user_id')

    class Meta:
        db_table = 'category'

class TaskModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks', db_column='category_id')
    shared_with = models.ManyToManyField(User, related_name='shared_tasks', blank=True)
    priority = models.CharField(choices=PriorityOptions, default=PriorityOptions.MEDIUM, max_length=50)
    status = models.CharField(choices=StatusTask, default=StatusTask.PENDING, max_length=50)

    class Meta:
        db_table = 'task'
 