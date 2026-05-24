from django.db import models

class PriorityOptions(models.TextChoices):
        HIGH = 'ALTA', 'Prioridade Alta'
        MEDIUM = 'MEDIA', 'Prioridade Média'
        LOW = 'BAIXA', 'Prioridade Baixa'

class StatusTask(models.TextChoices):
        PENDING = 'PENDENTE', 'Status pendente'
        IN_PROGRESS = 'EM_PROGRESSO', 'Status em progresso'
        COMPLETED = 'CONCLUIDO', 'Status concluido'
        