from flask import Flask, request
from flask_cors import CORS
from json import dumps, loads
from bson.objectid import ObjectId
from db_connect import find_user, add_user, get_team_users, get_team_projects, get_project_details, add_new_project, \
    mission_accomplished
from login_token import certify_token, generate_token

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_data = loads(request.data.decode())
        if valid_login(post_data):
            return dumps({'status': 'success',
                          'token': generate_token(post_data['userName'], 3600),
                          'userName': post_data['userName']
                          })
        else:
            return dumps({'status': 'fail'})


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = loads(request.data.decode())
        return add_user(data)


@app.route('/getUsers', methods=['GET'])
def get_users():
    print(request.headers.get('token'))
    if not certify_token(token=request.headers.get('token'), key=request.headers.get('username')):
        return dumps({'success': False, 'reason': '您的token已失效'})
    else:
        response = get_team_users({'userName': request.headers.get('username')})
        response['success'] = True
        return dumps(response)


@app.route('/getProjects', methods=['GET'])
def get_projects():
    if not certify_token(token=request.headers.get('token'), key=request.headers.get('username')):
        return dumps({'success': False, 'reason': '您的token已失效'})
    else:
        response = get_team_projects({'userName': request.headers.get('username')})
        response['success'] = True
        return dumps(response)


@app.route('/getProjectDetail', methods=['GET'])
def get_project_detail():
    if not certify_token(token=request.headers.get('token'), key=request.headers.get('username')):
        return dumps({'success': False, 'reason': '您的token已失效'})
    else:
        response = get_project_details({'_id': ObjectId(request.args.get('id'))})
        response['success'] = True
        return dumps(response)


@app.route('/addProject', methods=['POST'])
def add_project():
    if not certify_token(token=request.headers.get('token'), key=request.headers.get('username')):
        return dumps({'success': False, 'reason': '您的token已失效'})
    else:
        data = loads(request.data.decode())
        if add_new_project(options={'userName': request.headers.get('username')}, data=data):
            return dumps({'success': True, 'project_name': data['project_name']})
        else:
            return dumps({'success': False, 'reason': '新建项目失败'})


@app.route('/item_accomplished', methods=['GET'])
def item_accomplished():
    if not certify_token(token=request.headers.get('token'), key=request.headers.get('username')):
        return dumps({'success': False, 'reason': '您的token已失效'})
    else:
        response = mission_accomplished(request.args.get('id'))
        print(response)
        response['success'] = True
        response['_id'] = str(response['_id'])
        response['deadline'] = response['deadline'].strftime('%Y-%m-%d')
        return dumps(response)


def valid_login(options):
    # print(options)
    res = find_user(options)
    # print(res)
    if res is None:
        return False
    else:
        return True


if __name__ == '__main__':
    app.run(debug=True)
