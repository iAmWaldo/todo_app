from django.contrib import admin
from .models import List, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'priority', 'status')


class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title')


admin.site.register(List, ListAdmin)
admin.site.register(Task, TaskAdmin)
