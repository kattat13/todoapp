from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('signup/', views.signup_user, name='signup_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # todos
    path('home/', views.home, name='home'),
    path('current/', views.current_todos, name='current_todos'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('create/', views.create_task, name='create_task'),
    path('task/<int:task_pk>', views.view_task, name='view_task'),
    path('task/<int:task_pk>/done', views.done, name='done'),
    path('task/<int:task_pk>/del', views.delete, name='delete'),

    # API
    path('api/', include('api.urls')),

]
