from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView  # , CreateView
from .models import List, Task
from .forms import CreateList, CreateTask
from django.contrib.auth.models import User


@login_required
def home(request):
    user = User.objects.get(id=request.user.id)
    lists = user.list_set.all()
    # lists = List.objects.prefetch_related('tasks').all()
    context = {
        'lists': lists,
    }
    return render(request, 'todo/home.html', context)


@login_required
def list_view(request, list_id):
    if request.method == 'POST':
        for key in request.POST:
            if 'delete-list' == key:
                delete_list(request, list_id)
                return redirect('home')
            else:
                form = CreateTask(request.user, request.POST, request.FILES)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.list = List.objects.get(id=list_id)
                    data.owner = request.user
                    data.save()
                    return redirect('list-details', list_id=list_id)
    else:
        form = CreateTask(request.user)

    t_list = List.objects.get(id=list_id)
    if t_list.owner == request.user:
        user = User.objects.get(id=request.user.id)
        list = user.list_set.prefetch_related('tasks').get(id=list_id)
    else:
        messages.warning(request, "You don't have access to this list!")
        return redirect('home')

    # list = List.objects.prefetch_related('tasks').get(id=list_id)
    context = {
        'list': list,
        'form': form,
    }
    return render(request, 'todo/list-details.html', context)


@login_required
def task_view(request, pk):
    if request.method == 'POST':
        if 'delete-task' in request.POST:
            list_id = update_task(request, pk)
            return redirect('list-details', list_id=list_id)
        else:
            update_task(request, pk)
    t_task = Task.objects.get(id=pk)
    if t_task.list.owner == request.user:
        task = Task.objects.get(id=pk)
    else:
        messages.warning(request, "You don't have access to this task")
        return redirect('home')
    context = {
        'task': task,
    }
    return render(request, 'todo/task-details.html', context)


class TaskModifyView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = [
        'title',
        'description',
        'file',
    ]

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.list.owner:
            return True
        return False

# class ListCreateView(LoginRequiredMixin, CreateView):
#     model = List
#     template_name = 'todo/create-list.html'
#     fields = ['title']


@login_required
def create_list_view(request):
    if request.method == 'POST':
        form = CreateList(request.POST)
        if form.is_valid():
            list = form.save(commit=False)
            list.owner = request.user
            list.save()
            return redirect('list-details', list.id)
    else:
        form = CreateList()
    context = {
        'form': form,
    }
    return render(request, 'todo/create-list.html', context)


@login_required
def update_task(request, task_id):
    validation_status_inc = tuple(
        item for (item, value) in Task.status_choices if item != Task.status_choices[-1][0])
    validation_status_dec = tuple(
        item for (item, value) in Task.status_choices if item != Task.status_choices[0][0])
    status_list = tuple(item for (item, value) in Task.status_choices)

    validation_priority_inc = tuple(
        item for (item, value) in Task.priority_levels_choices if item != Task.priority_levels_choices[-1][0])
    validation_priority_dec = tuple(
        item for (item, value) in Task.priority_levels_choices if item != Task.priority_levels_choices[0][0])
    priority_list = tuple(item for (item, value) in Task.priority_levels_choices)

    if Task.objects.get(id=task_id).list.owner == request.user:
        task = Task.objects.get(id=task_id)
        print('################')
    else:
        messages.warning(request, "You don't have access to this task.")
        return redirect('home')

    # task = Task.objects.get(id=task_id)
    message = ''

    for key in request.POST:
        print(key)
        if 'increase-status' == key:
            if task.status in validation_status_inc:
                i = validation_status_inc.index(task.status) + 1
                Task.objects.filter(id=task_id).update(status=status_list[i])
            else:
                message = 'This is the highest status level available'

        elif 'decrease-status' == key:
            if task.status in validation_status_dec:
                i = validation_status_dec.index(task.status)
                Task.objects.filter(id=task_id).update(status=status_list[i])
            else:
                message = 'This is the lowest status level available'

        elif 'increase-priority' == key:
            if task.priority in validation_priority_inc:
                i = validation_priority_inc.index(task.priority) + 1
                Task.objects.filter(id=task_id).update(priority=priority_list[i])
            else:
                message = 'This is the highest priority level available'

        elif 'decrease-priority' == key:
            if task.priority in validation_priority_dec:
                i = validation_priority_dec.index(task.priority)
                Task.objects.filter(id=task_id).update(priority=priority_list[i])
            else:
                message = 'This is the lowest priority level available'

        elif 'delete-task' == key:
            task = Task.objects.get(id=task_id)
            list_id = task.list.id
            delete_task(request, task_id)
            return list_id

        if message != '':
            messages.info(request, message)


@login_required
def delete_task(request, task_id):
    if Task.objects.get(id=task_id).list.owner == request.user:
        Task.objects.get(id=task_id).delete()
    else:
        messages.warning(request, "You don't have access to this task.")
        return redirect('home')


@login_required
def delete_list(request, list_id):
    if List.objects.get(id=list_id).owner == request.user:
        List.objects.get(id=list_id).delete()
    else:
        messages.warning(request, "You don't have access to this list.")
        return redirect('home')
