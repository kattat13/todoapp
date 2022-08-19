from django.forms import ModelForm
from .models import Task


class TodoForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'important', 'deadline']
