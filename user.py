# coding:utf-8

import os
from base import Base
from common.utils import timestamp_to_string
from common.error import NotUserError, RoleError, UserActiveError

class User(Base):
    def __init__(self, username, user_json, gift_json):
        self.username = username

        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()

        if self.username not in users:
            raise NotUserError('not user %s' % self.username)

        current_user = users.get(self.username)

        if current_user.get('active') == False:
            raise UserActiveError('the user %s had not use' % self.username)

        if current_user.get('role') != 'normal':
            raise RoleError('permission by normal')

        self.name = current_user.get('username')
        self.role = current_user.get('role')
        self.gifts = current_user.get('gifts')
        self.create_time = timestamp_to_string(current_user.get('create_time'))

    def get_gifts(self):
        gifts = self._Base__read_gifts()
        gift_list = []

        for level_one, level_one_pool in gifts.items():
            for level_two, level_two_pool in level_one_pool.items():
                for gift_name, gift_info in level_two_pool.items():
                    gift_list.append(gift_info.get('name'))
        return gift_list


if __name__ == '__main__':
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    user = User('小慕', user_path, gift_path)
    result = user.get_gifts()
    print(result)


