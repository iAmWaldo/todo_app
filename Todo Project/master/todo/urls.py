from django.urls import path

from .views import (list_view,
                    home,
                    task_view,
                    create_list_view,
                    TaskModifyView)

urlpatterns = [
    path('', home, name='home'),
    path('list_id/<int:list_id>/', list_view, name='list-details'),
    path('task_id/<int:pk>/', task_view, name='task-details'),
    path('create_list/', create_list_view, name='create-list'),
    # path('create_list/', ListCreateView.as_view(), name='create-list'),
    path('task_id/<int:pk>/update', TaskModifyView.as_view(), name='update-task'),
]
