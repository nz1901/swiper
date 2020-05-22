from common import keys
from libs.http import render_json
from social import logics
from user.models import User
from vip.logics import need_perm
from libs.cache import rds
from swiper import config


def get_recd_list(request):
    data = logics.get_recd_list(request.uid)
    return render_json(data=data)


def like(request):
    sid = int(request.GET.get('sid'))
    uid = request.uid
    flag = logics.like(uid, sid)
    rds.zincrby(config.TOP_N, config.LIKE_SCORE, keys.TOP_N_KEY % sid)
    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


def dislike(request):
    # 创建一条mark为不喜欢的Swiped记录.
    # 检查一下是否有好友关系,如果有的话,删除好友关系.
    uid = request.uid
    sid = int(request.GET.get('sid'))
    logics.dislike(uid, sid)
    rds.zincrby(config.TOP_N, config.DISLIKE_SCORE, keys.TOP_N_KEY % sid)
    return render_json()


@need_perm('superlike')
def superlike(request):
    sid = int(request.GET.get('sid'))
    uid = request.uid
    flag = logics.superlike(uid, sid)
    rds.zincrby(config.TOP_N, config.SUPERLIKE_SCORE, keys.TOP_N_KEY % sid)
    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


@need_perm('rewind')
def rewind(request):
    # 反悔功能.
    # 只能反悔上一次滑动
    # 其实反悔就是把最近的一条Swiped记录删掉.
    # 一天只要3次反悔次数.返回的次数可以记录在redis中.
    uid = request.uid
    if logics.rewind(uid):
        return render_json()


def show_friends(request):
    # 从Friend表中查出uid是当前登录用户的id,或者sid是当前登录用户的id.]
    uid = request.uid
    data = logics.show_friends(uid)
    return render_json(data=data)


def top_n(request):
    data = logics.get_top_n()
    return render_json(data=data)
