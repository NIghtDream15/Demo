# coding:utf-8

import os
import time
import json

from common.utils import check_file, timestamp_to_string
from common.error import (UserExistsError, RoleError,
                          LevelError, NegativeNumberError, CountError)
from common.consts import ROLES, FIRSTLEVEL, SECONDLEVEL


class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json

        self.__check_user_json()
        self.__check_gift_json()
        self.__init_gifts()

    # 导入user.json 文件检查
    def __check_user_json(self):
        check_file(self.user_json)

    # 导入gift.json 文件检查
    def __check_gift_json(self):
        check_file(self.gift_json)

    # 读取用户信息
    def __read_users(self, time_to_str=False):
        with open(self.user_json, 'r', encoding='utf-8') as f:
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
        self.__save(users, self.user_json)

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
        users[username] = user
        self.__save(users, self.user_json)
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
        self.__save(users, self.user_json)
        return True

    # 删除用户
    def __delete_user(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False

        delete_user = users.pop(username)
        self.__save(users, self.user_json)
        return delete_user

    # 奖品读取
    def __read_gifts(self):
        with open(self.gift_json,encoding='utf-8') as f:
            data = json.loads(f.read())
        return data

    # 奖品列表初始化
    def __init_gifts(self):
        data = {
            'level1':{
                'level1':{},
                'level2':{},
                'level3':{}
            },
            'level2': {
                'level1': {},
                'level2': {},
                'level3': {}
            },
            'level3': {
                'level1': {},
                'level2': {},
                'level3': {}
            },
            'level4': {
                'level1': {},
                'level2': {},
                'level3': {}
            }
        }
        gifts = self.__read_gifts()
        if len(gifts) != 0:
            return
        self.__save(data, self.gift_json)

    # 奖品添加
    def __write_gift(self, first_level, second_level, gift_name, gift_count):

        if first_level not in FIRSTLEVEL:
            raise LevelError('firstlevel not exists')
        if second_level not in SECONDLEVEL:
            raise LevelError('secondlevel not exits')

        gifts = self.__read_gifts()

        current_gift_pool = gifts[first_level]
        current_second_gift_pool = current_gift_pool[second_level]

        if gift_count <= 0:
            gift_count = 1

        if gift_name in current_second_gift_pool:
            current_second_gift_pool[gift_name]['count'] = current_second_gift_pool[gift_name]['count'] + gift_count
        else:
            current_second_gift_pool[gift_name] = {
                'name': gift_name,
                'count': gift_count
            }

        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        self.__save(gifts, self.gift_json)

        gifts = self.__read_gifts()
        print(gifts)

    def __gift_update(self, first_level, second_level,
                      gift_name, gift_count=1, is_admin=False):

        assert isinstance(gift_count, int), 'gift count is a int'
        data = self.__check_and_getgift(first_level, second_level, gift_name)

        if data == False:
            return data

        current_gift_pool = data.get('level_one')
        current_second_gift_pool = data.get('level_two')
        gifts = data.get('gifts')

        current_gift = current_second_gift_pool[gift_name]

        if is_admin == True:
            if gift_count <= 0:
                raise CountError('gift count not 0')
            current_gift['count'] = gift_count
        else:
            if current_gift['count'] - gift_count < 0:
                raise NegativeNumberError('gift count cannot negative')
            current_gift['count'] -= gift_count

        current_second_gift_pool[gift_name] = current_gift
        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        self.__save(gifts, self.gift_json)

    def __check_and_getgift(self, first_level, second_level, gift_name):
        if first_level not in FIRSTLEVEL:
            raise LevelError('firstlevel not exists')
        if second_level not in SECONDLEVEL:
            raise LevelError('secondlevel not exits')

        gifts = self.__read_gifts()

        level_one = gifts[first_level]
        level_two = level_one[second_level]

        if gift_name not in level_two:
            return False

        return {
            'level_one': level_one,
            'level_two': level_two,
            'gifts': gifts
        }

    def __delete_gift(self, first_level, second_level, gift_name):
        data = self.__check_and_getgift(first_level, second_level, gift_name)

        if data == False:
            return data

        current_gift_pool = data.get('level_one')
        current_second_gift_pool = data.get('level_two')
        gifts = data.get('gifts')

        delete_gift_data = current_second_gift_pool.pop(gift_name)
        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        self.__save(gifts, self.gift_json)
        return delete_gift_data


    def __save(self, data, path):
        json_data = json.dumps(data, ensure_ascii=False) # ensure_ascii解决中文显示\u编码问题
        with open(path, 'w',encoding='utf-8') as f:
            f.write(json_data)




if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    print(gift_path)
    print(user_path)
    base = Base(user_json=user_path, gift_json=gift_path)
    # base.delete_gift(first_level='level1', second_level='level2', gift_name='apple10')
    base.change_role(username='小慕', role='normal')
    # result = base.delete_user(username='dewei')
    # print(result)