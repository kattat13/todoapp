from rest_framework import generics, permissions
from .serializers import TaskSerializer, TaskDoneSerializer
from todo.models import Task
from django.utils import timezone
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from django.http import JsonResponse
# from django.db import IntegrityError
# from django.contrib.auth.models import User
# from django.contrib.auth import login


# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         try:
#             data = JSONParser().parse(request)
#             user = User.objects.create_user(data['username'], password=data['password'])
#             user.save()
#             # token = Token.objects.create(user=user)
#             return JsonResponse({'token': 'tokennn'}, status=201)
#         except IntegrityError:
#             return JsonResponse({'error':'That username has already been taken. Please choose a new username'}, status=400)
        

class TaskCompletedList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user, completed_date__isnull=False).order_by('-completed_date')


class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user, completed_date__isnull=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        
class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)


class TaskDone(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed_date = timezone.now()
        serializer.save()


