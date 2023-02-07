# coding:utf-8

# 路径错误
class NotPathError(Exception):
    def __init__(self, message):
        self.message = message


# 格式错误
class FormatError(Exception):
    def __init__(self, message):
        self.message = message


# 文件错误
class NotFileError(Exception):
    def __init__(self, message):
        self.message = message


# 用户已存在
class UserExistsError(Exception):
    def __init__(self, message):
        self.message = message

# 角色错误
class RoleError(Exception):
    def __init__(self, message):
        self.message = message