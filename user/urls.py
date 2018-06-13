# /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Allen
@contact: 809721414@qq.com
@time: 2018/5/10 11:54
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('register', views.add_user, name='register'),
    path('choose_team', views.choose_team, name='choose_team'),
    path('get_all_teams', views.get_all_teams, name='get_all_teams'),
    path('get_user_teams', views.get_uer_teams, name='get_user_teams'),
    path('create_team', views.create_team, name='create_team'),
    path('get_team_users', views.get_team_users, name='get_team_users'),
    path('file_upload', views.file_upload, name='file_upload'),
    path('change_username', views.change_username, name='change_username'),
    path('get_user', views.get_user_info, name='get_user'),
    path('deleteUser', views.delete_user_from_team, name='deleteUser'),
    path('changePhoneNumber', views.change_user_phone_number, name='changePhoneNumber')
]
