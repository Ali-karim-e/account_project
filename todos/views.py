from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateTodo, TodosSearchForm, EditeTodo
from .models import Todos
from datetime import datetime


class TodoCreateView(View):
    form_class = CreateTodo
    template_name = 'todos/create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '!!Please log in syte!!')
            return redirect('todos:todos')
        elif not request.user.is_admin:
            messages.warning(request, '!!You not permission !!')
            return redirect('todos:todos')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            todos = Todos(title=cd['title'], desc=cd['desc'], Functor=cd['Functor'])
            todos.save()
            messages.success(request, 'Create todos successfully', 'success')
            return redirect('todos:todos')
        return render(request, self.template_name, {'form': form})


class Todos_view(View):
    model = Todos
    template_name = 'todos/index.html'
    form_class = TodosSearchForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Welcome !! Please log in syte!!')
            return render(request, self.template_name, {'form': self.form_class})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if request.user.is_admin:
            todos = Todos.objects.all()
        else:
            todos = Todos.objects.filter(Functor=request.user.id,active=1)
        if request.GET.get('search'):
            todos = todos.filter(body__contains=request.GET['search'])
        return render(request, self.template_name, {'todos': todos, 'form': self.form_class})

class TodosEdit_View(View):
    model = Todos
    template_name = 'todos/edit.html'
    form_class = EditeTodo
    def get(self, request, todos_id):
        todos = Todos.objects.get(pk=todos_id)
        form = self.form_class(initial={
                'done':todos.done,
                'descend':todos.descend,
                'attachment':todos.attachment,
            })
        return render(request, self.template_name, {'form': form, 'todos':todos})

    def post(self, request,todos_id):
        todos = Todos.objects.get(pk=todos_id)
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            todos.done = cd['done']
            todos.descend = cd['descend']
            todos.attachment = cd['attachment']
            todos.donedate = datetime.now()
            todos.save()
            messages.success(request, 'Edit todos is successfully end !!! ', 'success')
            return redirect('todos:todos')
        return render(request, self.template_name, {'form': form})


