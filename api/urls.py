from django.urls import path
from . import views

urlpatterns = [
    path('tasks/completed', views.TaskCompletedList.as_view()),
    path('tasks', views.TaskListCreate.as_view()),
    path('tasks/<int:pk>', views.TaskRetrieveUpdateDestroy.as_view()),
    path('tasks/<int:pk>/done', views.TaskDone.as_view()),

    path('signup', views.signup),
    
]