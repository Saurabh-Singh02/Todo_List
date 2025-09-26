from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Todo
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TodoForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('todo_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('todo_list')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    
    # Filtering
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'completed':
        todos = todos.filter(completed=True)
    elif filter_type == 'active':
        todos = todos.filter(completed=False)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        todos = todos.order_by('created_at')
    elif sort_by == 'priority':
        todos = todos.order_by('-priority')
    
    return render(request, 'todo/todo_list.html', {
        'todos': todos,
        'filter_type': filter_type,
        'sort_by': sort_by
    })

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Todo created successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm()
    
    return render(request, 'todo/todo_form.html', {'form': form, 'title': 'Create Todo'})

@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todo/todo_form.html', {'form': form, 'title': 'Update Todo'})

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
        return redirect('todo_list')
    
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

@login_required
def todo_toggle_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'completed': todo.completed})
    
    return redirect('todo_list')