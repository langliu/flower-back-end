from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import models
from qiniu import Auth, put_file

AK = 'Be4yzMaDNQenNaMcAHWMkLWTk05uyyRmL9yW-FMp'
SK = 'uROOPs_pDB_gRsCn4OI_2nGDvK2HhrQ0UBdrbUw2'
q = Auth(AK, SK)

# 要上传的空间
bucket_name = 'flower'


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            user = models.User.objects.get(email=request.POST.get('email'), password=request.POST.get('password'))
        except models.User.DoesNotExist:
            user = None
        if user:
            return JsonResponse({
                'success': True,
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'active_team': user.active_team,
                    'token': user.email
                }
            })
        else:
            return JsonResponse({'success': False, 'reason': '用户名或密码错误'})


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        user = request.POST.dict()
        if models.User.objects.has_email(email=user['email']):
            return JsonResponse({'success': False, 'reason': '该邮箱已注册'})
        elif models.User.objects.has_phone_number(phone_number=user['phone_number']):
            return JsonResponse({'success': False, 'reason': '该手机号已注册'})
        else:
            models.User.objects.create(
                username=user['username'],
                password=user['password'],
                email=user['email'],
                phone_number=user['phone_number'])
            return JsonResponse({'success': True})


@csrf_exempt
def choose_team(request):
    """
    更改用户当前激活的team
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 用户邮箱
        email = request.META.get('HTTP_EMAIL')
        # 从表单中提取团队id
        team_id = request.POST.get('team_id')
        # 用户信息
        user = models.User.objects.get(email=email)
        # 修改用户当前激活的team
        user.active_team = int(team_id)
        user.save()
        return JsonResponse({'success': True})


@csrf_exempt
def get_all_teams(request):
    if request.method == 'GET':
        # 数据库中的所有团队
        teams = models.Team.objects.all()
        team_list = []
        for team in teams:
            team_list.append({'team_id': team.team_id, 'team_name': team.team_name})
        return JsonResponse({'success': True, 'teams': team_list})


@csrf_exempt
def get_uer_teams(request):
    if request.method == 'GET':
        # 用户邮箱
        email = request.META.get('HTTP_EMAIL')
        # 用户参与的团队
        team_list = get_user_team_by_email(email)
        return JsonResponse({'success': True, 'teams': team_list})


@csrf_exempt
def create_team(request):
    """
    创建新的团队
    :param request: 请求数据
    :return: json()
    """
    if request.method == 'POST':
        # 用户邮箱
        email = request.META.get('HTTP_EMAIL')
        user = models.User.objects.get(email=email)
        # 新建团队
        new_team = models.Team.objects.create_team(team_name=request.POST.get('team_name'))
        # 修改用户当前激活的团队
        user.active_team = new_team.team_id
        user.save()
        # 添加team和user的关系，默认为超级管理员
        models.TeamUser.objects.create_team_user(
            team_id=new_team.team_id,
            user_id=user.user_id,
            user_permission='2')
        return JsonResponse({})


@csrf_exempt
def get_team_users(request):
    if request.method == 'GET':
        team_id = request.GET.get('active_team')
        try:
            team = models.Team.objects.get(team_id=team_id)
        except models.Team.DoesNotExist:
            team = None
        user_lists = []
        users = models.TeamUser.objects.filter(team_id=team_id)
        for us in users:
            try:
                one_user = models.User.objects.get(user_id=us.user_id)
            except models.User.DoesNotExist:
                return JsonResponse({'success': False})
            user_lists.append({
                'user_id': one_user.user_id,
                'username': one_user.username,
                'email': one_user.email,
                'phone_number': one_user.phone_number,
                'permission': us.user_permission
            })
        return JsonResponse({
            'success': True,
            'team_id': team.team_id,
            'team_name': team.team_name,
            'teamMembers': len(user_lists),
            'user_list': user_lists
        })


def get_user_team_by_email(email):
    """
    通过email获取用户已加入的team
    :param email: str(用户的email)
    :return: list(用户已加入的team列表)
    """
    user_id = models.User.objects.get(email=email).user_id
    teams = models.TeamUser.objects.filter(user_id=user_id)
    team_list = []
    for team in teams:
        team_message = models.Team.objects.get(team_id=team.team_id)
        team_list.append({'team_id': team_message.team_id, 'team_name': team_message.team_name})
    return team_list


@csrf_exempt
def file_upload(request):
    if request.method == 'POST':
        print(request)
        return JsonResponse({})


@csrf_exempt
def change_username(request):
    if request.method == 'POST':
        print(request.POST.dict())
        try:
            user = models.User.objects.get(user_id=request.POST.get('user_id'))
        except models.User.DoesNotExist:
            user = None
        user.username = request.POST.get('username')
        user.save()
        return JsonResponse({'success': True})


@csrf_exempt
def get_user_info(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        try:
            user = models.User.objects.get(user_id=user_id)
        except models.User.DoesNotExist:
            user = None
        if user is None:
            response = {'success': False, 'reason': '该用户不存在或其他错误'}
        else:
            response = {
                'success': True,
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'avatar': user.avatar,
                    'phone_number': user.phone_number,
                    'email': user.email,
                }
            }
        return JsonResponse(response)


@csrf_exempt
def delete_user_from_team(request):
    if request.method == 'POST':
        post_data = request.POST.dict()
        try:
            team_user = models.TeamUser.objects.get(team_id=post_data['teamId'], user_id=post_data['userId'])
        except models.TeamUser.DoesNotExist:
            team_user = None
        print(team_user)
        team_user.delete()
        return JsonResponse(post_data)


@csrf_exempt
def change_user_phone_number(request):
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)
        try:
            user = models.User.objects.get(user_id=request.POST.get('userId'))
        except models.User.DoesNotExist:
            user = None
        if user.password == data.get('password'):
            user.phone_number = data.get('phoneNumber')
            user.save()
            response = {'success': True, 'user': {
                'user_id': user.user_id,
                'username': user.username,
                'avatar': user.avatar,
                'phone_number': user.phone_number,
                'email': user.email,
            }}
        else:
            response = {'success': False, 'reason': '密码错误'}
        return JsonResponse(response)
