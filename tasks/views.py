from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Task


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
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        if due_date and due_date < timezone.now().date().isoformat():
            messages.error(request, "Due date cannot be in the past.")
            return redirect('add_task')

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date or None
        )

        messages.success(request, "Task added successfully.")

        return redirect('task_list')

    return render(request, 'tasks/add_task.html')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()

    messages.success(request, "Task deleted successfully.")

    return redirect('task_list')

@login_required
def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    task.is_completed = not task.is_completed
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
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        if due_date and due_date < timezone.now().date().isoformat():
            messages.error(request, "Due date cannot be in the past.")
            return redirect('edit_task', task_id=task.id)

        task.title = title
        task.description = description
        task.due_date = due_date or None

        task.save()

        messages.success(request, "Task updated successfully.")

        return redirect('task_list')

    return render(request, 'tasks/edit_task.html', {'task': task})