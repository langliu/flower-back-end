# /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Allen
@contact: 809721414@qq.com
@time: 2018/5/15 22:49
"""
from django.urls import path
from . import views

urlpatterns = [
    path('get_projects_by_team', views.get_projects_by_team, name='get_projects_by_team'),
    path('create_project', views.create_project, name='create_project'),
    path('create_project_list', views.create_project_list, name='create_project_list'),
    path('create_list_item', views.create_list_item, name='create_list_item'),
    path('create_item_detail', views.create_item_detail, name='create_item_detail'),
    path('get_project_list_by_project', views.get_project_list_by_project, name='get_project_list_by_project'),
    path('complete_task', views.complete_task, name='complete_task'),
    path('update_item', views.update_list_item, name='update_item'),
    path('get_item_detail', views.get_item_detail, name='get_item_detail'),
    path('complete_task_item', views.complete_task_item, name='complete_task_item'),
    path('getMyTasks', views.get_my_projects, name='getMyTasks'),
    path('getCompletionStatusData', views.get_completion_status_data, name='getCompletionStatusData')
]
