from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from .models import *
from user.models import *


@csrf_exempt
def get_projects_by_team(request):
    if request.method == 'GET':
        team_id = request.GET.get('team_id')
        print(team_id)
        projects = []
        for project in Project.objects.filter(team_id=team_id):
            projects.append({
                'project_id': project.project_id,
                'project_name': project.project_name,
                'team_id': project.team_id
            })
        return JsonResponse({'success': True, 'projects': projects})


@csrf_exempt
def create_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        team_id = request.POST.get('team_id')
        new_project = Project.objects.create_project(project_name, team_id)
        return JsonResponse({
            'success': True,
            'project': {
                'project_name': new_project.project_name,
                'project_id': new_project.project_id,
                'team_id': new_project.team_id
            }
        })


@csrf_exempt
def create_project_list(request):
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        project_id = request.POST.get('project_id')
        new_list = ProjectList.objects.create_project_list(list_name, project_id)
        return JsonResponse({
            'success': True,
            'project_list': {
                'project_list_id': new_list.project_list_id,
                'list_name': new_list.list_name,
                'project_id': new_list.project_id
            }
        })


@csrf_exempt
def create_list_item(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        project_list_id = request.POST.get('project_list_id')
        new_list_item = ListItem.objects.create_list_item(title, project_list_id)
        return JsonResponse({
            'success': True,
            'list_item': {
                'title': new_list_item.title,
                'project_list_id': new_list_item.project_list_id
            }
        })


@csrf_exempt
def create_item_detail(request):
    if request.method == 'POST':
        value = request.POST.get('value')
        list_item_id = request.POST.get('list_item_id')
        new_item_detail = ItemDetail.objects.create_item_detail(value, list_item_id)
        return JsonResponse({
            'success': True,
            'item_detail': {
                'list_item_id': new_item_detail.list_item_id,
                'item_detail_id': new_item_detail.item_detail_id,
                'value': new_item_detail.value,
                'status': new_item_detail.status
            }
        })


@csrf_exempt
def get_project_list_by_project(request):
    if request.method == 'GET':
        project_id = request.GET.get('project_id')
        project_lists = []
        for project_list in ProjectList.objects.filter(project_id=project_id):
            project_list_item = []
            for item in ListItem.objects.filter(project_list_id=project_list.project_list_id):
                try:
                    username = User.objects.get(user_id=item.user_id).username
                except User.DoesNotExist:
                    username = None
                project_list_item.append({
                    'list_item_id': item.list_item_id,
                    'title': item.title,
                    'status': item.status,
                    'deadline': item.deadline,
                    'username': username
                })
            project_list_item.sort(key=lambda x: x['status'])
            project_lists.append({
                'project_list_id': project_list.project_list_id,
                'list_name': project_list.list_name,
                'project_list_item': project_list_item
            })
        return JsonResponse({
            'success': True,
            'project_list': project_lists
        })


@csrf_exempt
def complete_task(request):
    if request.method == 'GET':
        list_item_id = request.GET.get('list_item_id')
        try:
            item = ListItem.objects.get(list_item_id=list_item_id)
        except ListItem.DoesNotExist:
            return JsonResponse({'success': False})
        item.status = not item.status
        item.save()
        return JsonResponse({'success': True})


@csrf_exempt
def complete_task_item(request):
    if request.method == 'GET':
        item_detail_id = request.GET.get('item_detail_id')
        try:
            item = ItemDetail.objects.get(item_detail_id=item_detail_id)
        except ItemDetail.DoesNotExist:
            return JsonResponse({'success': False})
        item.status = not item.status
        item.save()
        num = 0
        sum_number = 0
        for i in ItemDetail.objects.filter(list_item_id=item.list_item_id):
            if i.status:
                num = num + 1
            sum_number = sum_number + 1
        return JsonResponse({'success': True, 'progress': num * 100 // sum_number})


@csrf_exempt
def update_list_item(request):
    if request.method == 'POST':
        post_data = request.POST.dict()
        try:
            item = ListItem.objects.get(list_item_id=post_data['list_item_id'])
        except ListItem.DoesNotExist:
            return JsonResponse({'success': False})
        if post_data.__contains__('user_id'):
            item.user_id = post_data['user_id']
        if post_data.__contains__('username'):
            item.user_id = User.objects.get(username=post_data['username']).user_id
        if post_data.__contains__('deadline'):
            item.deadline = post_data['deadline']
        if post_data.__contains__('description'):
            item.description = post_data['description']
        if post_data.__contains__('title'):
            item.title = post_data['title']
        if post_data.__contains__('project_list_id'):
            item.project_list_id = post_data['project_list_id']
        item.save()
        return JsonResponse({'success': True})


@csrf_exempt
def get_item_detail(request):
    if request.method == 'GET':
        list_item_id = request.GET.get('list_item_id')
        try:
            item = ListItem.objects.get(list_item_id=list_item_id)
        except ListItem.DoesNotExist:
            return JsonResponse({'success': False})
        tasks = []
        num = 0
        for i in ItemDetail.objects.filter(list_item_id=list_item_id):
            if i.status:
                num = num + 1
            tasks.append({
                'item_detail_id': i.item_detail_id,
                'value': i.value,
                'status': i.status
            })
        response = {
            'success': True,
            'item': {
                'list_item_id': item.list_item_id,
                'title': item.title,
                'status': item.status,
                'deadline': item.deadline,
                'description': item.description
            },
            'tasks': tasks
        }
        if len(tasks):
            response['progress'] = num * 100 // len(tasks),
        try:
            username = User.objects.get(user_id=item.user_id).username
        except User.DoesNotExist:
            username = None
        response['username'] = username
        return JsonResponse(response)


@csrf_exempt
def get_my_projects(request):
    if request.method == 'GET':
        user_id = request.GET.get('userId')
        today_tasks = []
        next_tasks = []
        complete_tasks = []
        for item in ListItem.objects.filter(user_id=user_id):
            task_list = ProjectList.objects.get(project_list_id=item.project_list_id)
            res = {
                'title': item.title,
                'deadline': item.deadline,
                'id': item.list_item_id,
                'listName': task_list.list_name,
                'status': item.status,
                'projectName': Project.objects.get(project_id=task_list.project_id).project_name
            }
            if res['status']:
                complete_tasks.append(res)
            elif res['deadline'] != datetime.date.today():
                next_tasks.append(res)
            else:
                today_tasks.append(res)
        return JsonResponse({'today': today_tasks, 'next': next_tasks, 'completed': complete_tasks})


@csrf_exempt
def get_completion_status_data(request):
    if request.method == 'GET':
        project_id = request.GET.get('projectId')
        task_list = []
        data = [
            {
                'name': '已完成',
                'value': 0
            },
            {
                'name': '未完成',
                'value': 0
            }
        ]
        for l in ProjectList.objects.filter(project_id=project_id):
            task_list.append(l.project_list_id)
        for task in ListItem.objects.filter(project_list_id__in=task_list):
            if task.status:
                data[0]['value'] += 1
            else:
                data[1]['value'] += 1
        return JsonResponse({'data': data})
