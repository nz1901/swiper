import datetime

from social.models import Swiped, Friend
from user.models import User


def get_recd_list(uid):
    now = datetime.datetime.now()
    user = User.objects.get(id=uid)
    # 根据最大最小交友年龄可以算出用户的出生区间.
    max_birth_year = now.year - user.profile.min_dating_age
    min_birth_year = now.year - user.profile.max_dating_age
    # 从swiped表中查询已经被当前用户滑过的人
    # 已经滑过的人就不要再出现在推荐了列表了.
    # 只需要被滑过的人的id
    swiped_list = Swiped.objects.filter(uid=uid).only('sid')
    # 取出sid
    sid_list = [s.sid for s in swiped_list]
    # 把自己也排除
    sid_list.append(uid)
    users = User.objects.filter(location=user.profile.dating_location,
                                birthday__range=[
                                    datetime.date(year=min_birth_year,
                                                  month=user.birthday.month,
                                                  day=user.birthday.day),
                                    datetime.date(year=max_birth_year,
                                                  month=user.birthday.month,
                                                  day=user.birthday.day)],
                                gender=user.profile.dating_gender) \
                .exclude(id__in=sid_list)[:20]
    data = [user.to_dict() for user in users]
    return data


def like(uid, sid):
    Swiped.like(uid, sid)
    # 判断对方是否喜欢过我们,如果是,则建立好友关系,
    if Swiped.has_like(uid=sid, sid=uid):
        # 说明对方也喜欢你.建立好友关系
        # 保证Friend中的uid1是比较小的id, uid2是大的id
        Friend.make_friends(uid, sid)
        return True
    return False


def dislike(uid, sid):
    Swiped.dislike(uid=uid, sid=sid)
    # 删除好友记录
    Friend.delete_friend(uid, sid)


def superlike(uid, sid):
    Swiped.superlike(uid, sid)
    # 判断对方是否喜欢过我们,如果是,则建立好友关系,
    if Swiped.has_like(uid=sid, sid=uid):
        # 说明对方也喜欢你.建立好友关系
        # 保证Friend中的uid1是比较小的id, uid2是大的id
        Friend.make_friends(uid, sid)
        return True
    return False
