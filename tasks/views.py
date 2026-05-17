from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Task


def get_priority_choices():
    return Task.PRIORITY_CHOICES


def is_valid_priority(priority):
    valid_priorities = [choice[0] for choice in Task.PRIORITY_CHOICES]
    return priority in valid_priorities


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    todo_count = tasks.filter(status='todo').count()
    in_progress_count = tasks.filter(status='in_progress').count()
    done_count = tasks.filter(status='done').count()

    context = {
        'tasks': tasks,
        'todo_count': todo_count,
        'in_progress_count': in_progress_count,
        'done_count': done_count,
    }

    return render(request, 'tasks/task_list.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date', '')
        priority = request.POST.get('priority', 'medium')

        context = {
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'priority_choices': get_priority_choices(),
        }

        if not title:
            messages.error(request, "Task title cannot be empty.")
            return render(request, 'tasks/add_task.html', context)

        if not is_valid_priority(priority):
            messages.error(request, "Invalid task priority.")
            return render(request, 'tasks/add_task.html', context)

        if due_date and due_date < timezone.now().date().isoformat():
            messages.error(request, "Due date cannot be in the past.")
            return render(request, 'tasks/add_task.html', context)

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date or None,
            priority=priority
        )

        messages.success(request, "Task added successfully.")
        return redirect('task_list')

    return render(request, 'tasks/add_task.html', {
        'priority_choices': get_priority_choices(),
        'priority': 'medium',
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('task_list')


@login_required
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if task.status == 'todo':
        task.status = 'in_progress'
        task.is_completed = False
    elif task.status == 'in_progress':
        task.status = 'done'
        task.is_completed = True
    else:
        task.status = 'todo'
        task.is_completed = False

    task.save()
    messages.success(request, "Task status updated successfully.")
    return redirect('task_list')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date', '')
        priority = request.POST.get('priority', 'medium')

        context = {
            'task': task,
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'priority_choices': get_priority_choices(),
        }

        if not title:
            messages.error(request, "Task title cannot be empty.")
            return render(request, 'tasks/edit_task.html', context)

        if not is_valid_priority(priority):
            messages.error(request, "Invalid task priority.")
            return render(request, 'tasks/edit_task.html', context)

        if due_date and due_date < timezone.now().date().isoformat():
            messages.error(request, "Due date cannot be in the past.")
            return render(request, 'tasks/edit_task.html', context)

        task.title = title
        task.description = description
        task.due_date = due_date or None
        task.priority = priority
        task.save()

        messages.success(request, "Task updated successfully.")
        return redirect('task_list')

    return render(request, 'tasks/edit_task.html', {
        'task': task,
        'priority_choices': get_priority_choices(),
    })