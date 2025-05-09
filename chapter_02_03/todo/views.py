from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from todo.models import Todo # 절대경로 import
from django.shortcuts import get_object_or_404
from todo.forms import TodoForm, TodoUpdateForm

# 전체 조회 및 페이지
@login_required
def todo_list(request):
    todo_list = Todo.objects.filter(user=request.user).order_by('-created_at')
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )
    paginator = Paginator(todo_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    result = [{'id': todo.id, 'title': todo.title} for todo in todo_list]
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'todo_list.html', context)

# 상세조회
@login_required
def todo_info(request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        context = {'todo':todo.__dict__}
        return render(request, 'todo_info.html', context)
# 생성
@login_required
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo_info', kwargs={'pk':todo.pk}))
    context = {'form':form}
    return render(request, 'todo_create.html', context)

# 수정
@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo_info', kwargs={'pk':pk}))
    context ={'form':form}
    return render(request, 'todo_create.html', context)

# 삭제
@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))





