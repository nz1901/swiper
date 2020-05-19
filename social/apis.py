import datetime

from libs.http import render_json
from social.models import Swiped, Friend
from user.models import User
from social import logics


def get_recd_list(request):
    data = logics.get_recd_list(request.uid)
    return render_json(data=data)


def like(request):
    sid = int(request.GET.get('sid'))
    uid = request.uid
    flag = logics.like(uid, sid)
    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


def dislike(request):
    # 创建一条mark为不喜欢的Swiped记录.
    # 检查一下是否有好友关系,如果有的话,删除好友关系.
    uid = request.uid
    sid = int(request.GET.get('sid'))
    logics.dislike(uid, sid)
    return render_json()


def superlike(request):
    sid = int(request.GET.get('sid'))
    uid = request.uid
    flag = logics.superlike(uid, sid)
    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})
