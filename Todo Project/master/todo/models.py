from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class List(models.Model):
    user = User.objects.get(id=3)
    owner = models.ForeignKey(User, default=user.id, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, default='')
    timestamp = models.DateTimeField(auto_now=True)
    # lists = models.Manager()  # basically replaces the name 'objects', by lists
    # now instead of using List.objects.all() we can use List.lists.all()

    def __str__(self):
        return self.title.capitalize()


class Task(models.Model):
    priority_levels_choices = (
        ('A', 'Low'),
        ('B', 'Normal'),
        ('C', 'High'),
        ('D', 'Very high'),
    )

    status_choices = (
        ('A', 'Not started'),
        ('B', 'In progress'),
        ('C', 'Completed'),
    )
    title = models.CharField(max_length=255, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=1000, choices=priority_levels_choices, default='Normal')
    status = models.CharField(max_length=1000, choices=status_choices, default='Not started')
    list = models.ForeignKey(List, on_delete=models.CASCADE, blank=False, related_name='tasks')
    blocked_by_a_task = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    blocked_by_a_list = models.ForeignKey(List, blank=True, null=True, on_delete=models.SET_NULL)
    file = models.FileField(blank=True, upload_to='task')

    # now List.task_set.all() == List.tasks.all()

    def __str__(self):
        return self.title.capitalize()

    def get_absolute_url(self):
        return reverse('task-details', kwargs={'pk': self.pk})

    def tasks_choices(self):
        pass

    # def is_blocked(self):
        # if self.blocked:
        # Task.blocked_by = models.CharField(choices=Task.priority_levels_choices)
