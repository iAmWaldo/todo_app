from .models import List, Task
from django import forms


class CreateList(forms.ModelForm):
    class Meta:
        model = List
        fields = [
            'title'
        ]


class CreateTask(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        #     print(kwargs)
        super(CreateTask, self).__init__(*args, **kwargs)
        # lists = List.objects.filter(owner=user)
        # tasks = user.task_set.all()
        self.fields['blocked_by_a_list'].queryset = List.objects.filter(owner=user)
        self.fields['blocked_by_a_task'].queryset = Task.objects.filter(owner=user)

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'priority',
            'status',
            'blocked_by_a_list',
            'blocked_by_a_task',
            'file',
        ]
        widgets = {
            'list': forms.HiddenInput(),
        }
