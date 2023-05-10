from django import forms
from .models import Todos


class CreateTodo(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ('title','desc','Functor')


class EditeTodo(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ('done','descend','attachment')


class TodosSearchForm(forms.Form):
    search = forms.CharField()