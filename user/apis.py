import re

from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from libs.sms import send_sms
from common import errors
from libs.http import render_json
from common import keys
from user.models import User


def submit_phone(request):
    """获取短信验证码"""
    phone = request.POST.get('phone')

    # 对phone做校验
    result = re.match(r'^1[3456789]\d{9}', phone)

    if not result:
        # 手机号码不合格
        # return JsonResponse({'code': errors.PHONE_ERROR, 'data': '手机号码格式有误'})
        return render_json(code=errors.PHONE_ERROR, data='手机号码格式有误')
    # 发送验证码
    flag = send_sms(phone)
    if flag:
        # 发送成功
        # return JsonResponse({'code': 0, 'data': '手机验证码发送成功'})
        return render_json()
    else:
        # return JsonResponse({'code': errors.SEND_VCODE_ERROR, 'data': '手机验证码发送失败'})
        return render_json(code=errors.SEND_VCODE_ERROR, data='手机验证码发送失败')


@require_http_methods(['POST'])
def submit_vcode(request):
    """通过验证码登录、注册"""
    # 用户提交收到短信验证, 接收之后,和刚才发送的短信验证做对比
    # 如果正确,就可以登录注册, 不正确,返回错误信息
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    # 从缓存中获取vcode
    key = keys.VCODE % phone
    cached_vcode = cache.get(key)
    print('vcode:', vcode)
    print('cached_vcode', cached_vcode)
    if vcode and vcode == cached_vcode:
        # 可以登录或注册
        # app的登录注册非常简单. 如果是第一次登录,那就注册一个新用户.
        # 如果在数据库中已经存在这个用户
        # try:
        #     user = User.objects.get(phonenum=phone)
        # except User.DoesNotExist:
        #     # 找不到用户说明是注册
        #     user = User.objects.create(phonenum=phone, nickname=phone)
        # User.objects.get_or_create()
        # 使用get_or_create进行优化
        user, _ = User.objects.get_or_create(phonenum=phone, defaults={'nickname': phone})
        # 把用户的id写入session
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')



def get_profile(request):
    """查看个人交友资料"""
    pass


def edit_profile(request):
    """修改个人资料、及交友资料"""
    pass


def upload_avatar(request):
    """头像上传"""
    pass



