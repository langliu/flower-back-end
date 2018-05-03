from json import dumps
from pymongo import MongoClient
from bson.objectid import ObjectId

mongodb_client = MongoClient('localhost', 27017)
db = mongodb_client.flower
user = db.User  # 用户表
team = db.Team  # 团队表
project = db.Project
project_item = db.Project_Item


def find_user(options):
    """
    查询用户是否存在
    :param options: dict(查询参数)
    :return:
    """
    result = user.find_one(options)
    # print(result)
    if result is None:
        return None
    else:
        del result['_id']
    return result


def add_user(options):
    """
    添加用户
    :param options: dict(用户数据)
    :return: str(添加结果)
    """
    print(options)
    if find_user({'userName': options['userName']}):
        response = dumps({'status': 'fail', 'reason': '用户名已存在'})
    elif find_user({'email': options['email']}):
        response = dumps({'status': 'fail', 'reason': '该邮箱已注册'})
    else:
        user.insert_one(options)
        response = dumps({'status': 'success'})
    return response


def get_team_users(options):
    """
    获取用户的团队成员
    :param options: dict(查询参数)
    :return: dict(查询结果)
    """
    team_id = user.find_one(options)['team']
    users = []
    for item in user.find({'team': team_id}):
        del item['_id']
        del item['team']
        users.append(item)
    print(users)
    return {'users': users, 'teamMembers': len(users), 'teamName': team.find_one({'_id': team_id})['team_name']}


def get_team_projects(options):
    """
    获取该团队的所有项目
    :param options: dict(查询参数)
    :return: dict(查询结果)
    """
    user_message = user.find_one(options)
    print(user_message)
    team_id = user_message['team']
    print(team_id)
    projects = project.find({'team': ObjectId(team_id)})
    project_list = []
    for p in projects:
        project_list.append({'id': str(p['_id']), 'project_name': p['project_name']})
    return {'project_list': project_list, 'team': str(team_id)}


def get_project_details(options):
    """
    获取项目详情
    :param options: dict(查询参数)
    :return: dict(项目详情)
    """
    response = {}
    res = project.find_one(options)
    response['project_name'] = res['project_name']
    project_list = res['project_list']
    response['project_list'] = []
    for pro in project_list:
        list_items = []
        for item in pro['list_items']:
            item_res = project_item.find_one({'_id': item})
            item_res['_id'] = str(item_res['_id'])
            item_res['deadline'] = item_res['deadline'].strftime('%Y-%m-%d')
            list_items.append(item_res)
        response['project_list'].append({
            'list_name': pro['list_name'],
            'list_items': list_items
        })
    return response


def add_new_project(options, data):
    """
    添加新的项目
    :param options: dict(插入选项)
    :param data: dict(要添加的数据)
    :return:
    """
    team_id = user.find_one(options)['team']
    data['team'] = team_id
    project.insert(data)
    if project.find_one(data):
        return data
    else:
        return False


print(get_project_details({'_id': ObjectId('5ae7e3f9e2c04342d42c2016')}))
