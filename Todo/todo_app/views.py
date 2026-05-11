from django.shortcuts import redirect, render
from .models import Task

# Create your views here.
def home(request):
    pending_tasks = Task.objects.filter(completed=False).order_by('-created_at')
    completed_tasks = Task.objects.filter(completed=True).order_by('-created_at')
    if request.method == 'POST':
        title = request.POST.get('task_title')
        description = request.POST.get('task_desc')
        if title:
            Task.objects.create(title=title, description=description, completed=False)
        return redirect('home')
    context = {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'todo/home.html', context)

def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('home')

def toggle_task(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = not task.completed
    task.save()
    return redirect('home')
