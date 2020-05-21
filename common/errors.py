"""所有的错误码放在这里"""

PHONE_ERROR = 1000
SEND_VCODE_ERROR = 1001
VCODE_ERROR = 1002
PROFILE_ERROR = 1003
LOGIN_REQUIRED = 1004
EXCEED_MAXIMUM_REWIND_TIMES = 1005


# 目标是产生一系列的自定义逻辑错误类.
# class PhoneError(Exception):
#     code = 1000
#     data = '手机号码格式错误'
#
# class SendVcodeError(Exception):
#     code = 1001
#     data = '发送手机验证码有误'

# 发现所有逻辑错误类写法都一样, 可以搞一个工厂函数来生产这些自定义逻辑错误类.
# 工厂模式.

# 逻辑错误类的模板
class LogicErr(Exception):
    code = None
    data = None


# 工厂模式
def gen_logic_err(name, code, data):
    return type(name, (LogicErr,), {'code': code, 'data': data})


# 生产上面这些自定义的逻辑错误类.
PhoneError = gen_logic_err('PhoneError', code=1000, data='手机号码格式错误')
SendVcodeError = gen_logic_err('SendVcodeError', code=1001, data='发送手机验证码有误')
VcodeError = gen_logic_err('VcodeError', code=1002, data='短信验证错误')
ProfileError = gen_logic_err('ProfileError', 1003, '个人交友资料错误')
LoginRequired = gen_logic_err('LoginRequired', 1004, '请登录')
ExceedMaximumRewindTimes = gen_logic_err('ExceedMaximumRewindTimes', 1005, '超过当日最大反悔次数')
