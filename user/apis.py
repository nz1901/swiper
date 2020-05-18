import re

from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from libs.sms import send_sms
from common import errors
from libs.http import render_json
from common import keys
from swiper import config
from user.models import User, Profile
from user import forms
from libs.qiniuyun import upload_qiniu

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
        return render_json(data=user.to_dict(exclude='id',))
    else:
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    """查看个人交友资料"""
    uid = request.uid
    user = User.objects.get(id=uid)
    # 用户的交友资料和用户是一对一的关系, 怎么实现一对一的关系?
    # 保证两张表的id是一致. user id = 1, 对应的profile id 也是1.
    # profile = Profile.objects.get(id=uid)
    return render_json(data=user.profile.to_dict(exclude=('id',)))


def edit_profile(request):
    """修改个人资料、及交友资料"""
    # 定义两个form表单的实例对象
    user_form = forms.UserForm(request.POST)
    profile_form = forms.ProfileForm(request.POST)

    # 检查user_form和profile_form
    if not user_form.is_valid() or not profile_form.is_valid():
        # 返回错误信息.
        form_errors = {}
        form_errors.update(user_form.errors)
        form_errors.update(profile_form.errors)
        return render_json(code=errors.PROFILE_ERROR, data=form_errors)

    # 如果form表单提交的数据没问题
    # 更新user和profile
    uid = request.uid
    # user_form.cleaned_data本身就是一个字典.可以使用**进行解包
    User.objects.filter(id=uid).update(**user_form.cleaned_data)

    # 更新或者创建profile
    # 注意: profile和user是一对一的关系, 创建profile的时候,为了满足一对一的关系.
    #  必须保证创建出来的profile的id和这个profile对应的user的id是一致.
    Profile.objects.update_or_create(id=uid, defaults=profile_form.cleaned_data)
    return render_json()


def upload_avatar(request):
    """头像上传"""
    # 先获取用户上传的文件.
    # 然后保存到本地
    # 然后上传到七牛云
    # 再然后使用七牛云的图片地址更新用户的avatar属性.
    avatar = request.FILES.get('avatar')
    # print(type(avatar))
    # print(avatar.name)
    # print(avatar.size)
    # print(avatar.content_type)
    # 保存到本地, 不要用用户上传的文件名.
    uid = request.uid
    filename = keys.AVATAR % uid
    # with open(f'./media/{filename}', mode='wb+') as fp:
    #     for chunk in avatar.chunks():
    #         fp.write(chunk)

    # 上传到七牛云
    upload_qiniu(avatar.read(), filename)
    # 修改user的avatar属性
    user = User.objects.get(id=uid)
    user.avatar = config.QN_URL + filename
    user.save()
    return render_json()



