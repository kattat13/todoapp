from dataclasses import fields
from rest_framework import serializers
from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_date = serializers.ReadOnlyField()
    completed_date = serializers.ReadOnlyField()
    done = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_date', 'important', 'done', 'completed_date']
        

class TaskDoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id']
        read_only_fields = ['name', 'description', 'created_date', 'important', 'done', 'completed_date']

