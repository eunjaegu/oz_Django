from django.http import Http404
from django.shortcuts import render
from todoList.models import Todo # 절대경로 import
from django.shortcuts import get_object_or_404

def todo_list(request):
    todo_list = Todo.objects.all()
    #result = [{'id': todo.id, 'title': todo.title} for todo in todo_list]
    # context = {
    #     'data': result,
    # }
    return render(request, 'todo_list.html', {'data':todo_list})

def todo_info(request, pk):
    #try:
        #todo = Todo.objects.get(pk=pk)
        # info = {
        #     'title': todo.title,
        #     'description': todo.description,
        #     'start_date' : todo.start_date,
        #     'end_date' : todo.end_date,
        #     'is_complete': todo.is_completed,
        # }

        todo = get_object_or_404(Todo, pk=pk)
        return render(request, 'todo_info.html', {'data':todo})
    # except Todo.DoesNotExist:
    #     raise Http404("Todo dees not exist")



