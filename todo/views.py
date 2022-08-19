from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task
from .forms import TodoForm


def home(request):
    return render(request, 'todo/home.html')


@login_required
def current_todos(request):
    tasks = Task.objects.filter(user=request.user, completed_date__isnull=True)
    return render(request, 'todo/current_tasks.html', {'tasks': tasks})


@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, completed_date__isnull=False).order_by('-completed_date')
    return render(request, 'todo/completed_tasks.html', {'tasks': tasks})


@login_required
def view_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)

    if request.method == 'GET':
        form = TodoForm(instance=task)
        return render(request, 'todo/view_task.html', {'task': task, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=task)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/view_task.html', {'task': task, 'form': form, 'error': 'Bad data passed in. Try again.'})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def done(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.completed_date = timezone.now()
        task.save()
        return redirect('current_todos')


@login_required
def delete(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('current_todos')


# auth

def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('current_todos')


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': "Username already taken. Please choose a new username."})
        else:
            return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': "Passwords don't match"})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')



