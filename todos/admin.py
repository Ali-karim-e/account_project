from django.contrib import admin
from .models import Todos

class TodosAdmin(admin.ModelAdmin):
    pass

admin.site.register(Todos, TodosAdmin)