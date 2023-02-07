# coding:utf-8

import os
import time
import json

from common.utils import check_file, timestamp_to_string
from common.error import UserExistsError, RoleError
from common.consts import ROLES


class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json

        self.__check_user_json()
        self.__check_gift_json()

    # 导入user.json 文件检查
    def __check_user_json(self):
        check_file(self.user_json)

    # 导入gift.json 文件检查
    def __check_gift_json(self):
        check_file(self.gift_json)

    # 读取用户信息
    def __read_users(self, time_to_str=False):
        with open(self.user_json, 'r') as f:
            data = json.loads(f.read())

        if time_to_str == True:
            for username, v in data.items():
                v['create_time'] = timestamp_to_string(v['create_time'])
                v['update_time'] = timestamp_to_string(v['update_time'])
                data[username] = v
        return data

    # 写入用户
    def __write_user(self, **user):
        if 'username' not in user:
            raise ValueError('missing username')
        if 'role' not in user:
            raise ValueError('missing role')

        user['active'] = True
        user['create_time'] = time.time()
        user['update_time'] = time.time()
        user['gifts'] = []

        # 如果用户存在报错
        users = self.__read_users()

        if user['username'] in users:
            raise UserExistsError('username %s is exist' % user['username'])

        # 如果用户不存在写入json
        users.update(
            {user['username']: user}
        )

        json_users = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_users)

    # 修改role
    def __change_role(self, username, role):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False

        if role not in ROLES:
            raise RoleError('not use role %s' % role)

        user['role'] = role
        user['update_time'] = time.time()
        users['username'] = user

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return True

    # active修改
    def __change_active(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False

        user['active'] = not user['active']
        user['update_time'] = time.time()
        users[username] = user

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return True

    # 删除用户
    def delete_user(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False

        delete_user = users.pop(username)

        json_data = json.dumps(users)
        with open(self.user_json, 'w') as f:
            f.write(json_data)
        return delete_user


if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    print(gift_path)
    print(user_path)
    base = Base(user_json=user_path, gift_json=gift_path)
    # base.write_user(username='dewei', role='admin')
    # result = base.delete_user(username='dewei')
    # print(result)