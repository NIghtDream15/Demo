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

# 奖品等级错误
class LevelError(Exception):
    def __init__(self, message):
        self.message = message

# 奖品数量错误
class NegativeNumberError(Exception):
    def __init__(self, message):
        self.message = message

# Admin用户名错误
class NotUserError(Exception):
    def __init__(self, message):
        self.message = message

# 用户状态错误
class UserActiveError(Exception):
    def __init__(self, message):
        self.message = message

# 数量错误
class CountError(Exception):
    def __init__(self, message):
        self.message = message