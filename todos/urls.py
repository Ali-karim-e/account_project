from django.urls import path
from . import views


app_name = 'todos'
urlpatterns = [
    path('', views.Todos_view.as_view(), name='todos'),
    path('create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('todos/<int:todos_id>/',views.TodosEdit_View.as_view(), name='todos_edit'),
   ]
