from django.http import Http404
from django.shortcuts import render
from todoList.models import Todo # 절대경로 import

def todo_list(request):
    todo_list = Todo.objects.all()
    result = [{'id': todo.id, 'title': todo.title} for todo in todo_list]
    context = {
        'data': result,
    }
    return render(request, 'todo_list.html', context)

def todo_info(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        info = {
            'title': todo.title,
            'description': todo,
            'start_date' : todo.start_date,
            'end_date' : todo.end_date,
            'is_complete': todo.is_completed,
        }
        return render(request, 'todo_info.html', {'data':info})
    except Todo.DoesNotExist:
        raise Http404("Todo dees not exist")



