from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .decorators import logout_required
from .recommender_engine.recommender import recommend_by_title
from django.core.files.storage import default_storage
from djangocrud.tasks import process_file
import os
from celery.result import AsyncResult
from django.urls import reverse

# Create your views here.

def home(request):
    return render(request, 'home.html')

@logout_required
def singup(request):

    if request.method == 'GET':
        return render(request, "singup.html", {
            'form' : UserCreationForm
            })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try: 
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/tasks')
                
            except IntegrityError:
                return render(request, "singup.html", {
                    'form' : UserCreationForm,
                    'error': 'User already exists' 
                    })
                
        return render(request, "singup.html", {
            'form' : UserCreationForm,
            'error': 'Passwords do not match'
            })

@logout_required
def singin(request):

    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
             return render(request, 'singin.html', {
            'form': AuthenticationForm,
            'error': 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
        
@login_required  
def singout(request):
    logout(request)
    return redirect('home')

@login_required  
def tasks(request): 
    tasks = Task.objects.filter(user_id=request.user, date_completed__isnull = True)
    return render(request, 'tasks.html', {'tasks': tasks, 'mode': 'Tasks Pending'})

@login_required  
def task_details(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user_id=request.user)
        form = CreateTaskForm(instance=task)
        return render (request, 'task_detail.html',{
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user_id=request.user)
            form = CreateTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render (request, 'task_detail.html',{
            'task': task,
            'form': form,
            'error': 'Error updating task'
        })

@login_required  
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': CreateTaskForm
        })
    else:
        try:
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit = False)
            new_task.user_id = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': CreateTaskForm,
                'error': 'Please provide valid data'
            })
        
@login_required  
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user_id=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required  
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user_id=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required  
def task_completed(request):
    tasks = Task.objects.filter(user_id=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'tasks.html', {'tasks': tasks, 'mode': 'Tasks Completed'})

@login_required  
def recomendator_form(request):
    recommendations = []
    query = ''

    if request.method == 'POST':
        query = request.POST.get('title_query', '').strip()
        recommendations = recommend_by_title(query)

    return render(request, 'recomender/form.html', {
        'recommendations': recommendations,
        'query': query,
    })

@login_required
def analyze_dataset(request):
    answer = None
    error = None
    task_id = request.GET.get("task_id")

    if request.method == 'POST':
        file = request.FILES.get('file')
        question = request.POST.get('question')

        if not file or not question:
            error = 'No question or file provided'
        else:
            try:
                file_path = default_storage.save(f"tmp/{file.name}", file)
                abs_path = os.path.join(default_storage.location, file_path)
                task = process_file.delay(abs_path, question)
                return redirect(f"{reverse('analyzer_form')}?task_id={task.id}")
            except Exception as e:
                error = f"Error: {str(e)}"

    elif task_id:
        result = AsyncResult(task_id)
        if result.ready():
            if result.successful():
                answer = result.result
            else:
                error = str(result.result) or "There was an error processing the file"
        else:
            # Task is still processing
            return render(request, 'analyzer/analyzer.html', {
                'loading': True,
                'task_id': task_id
            })

    return render(request, 'analyzer/analyzer.html', {
        'answer': answer,
        'error': error,
        'loading': False
    })