from common import errors
from user.models import User


def need_perm(perm_name):
    def wrapper(view_func):
        def inner(request, *args, **kwargs):
            # 判断当前登录用户是否具有perm_name权限
            # 用户和权限之间是没有直接的关系
            # 不能说用户是否具有某权限, 而应该说用户说在的vip等级是否具有某个权限.
            # 找到用户的vip, 然后判断vip中是否具有此权限.
            user = User.objects.get(id=request.uid)
            if user.vip.has_perm(perm_name):
                return view_func(request, *args, **kwargs)
            else:
                raise errors.PermissonDenied
        return inner
    return wrapper
