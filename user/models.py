import random

from django.db import models
from django.core.cache import cache

from common import keys
from libs.mixins import ModelMixin
from vip.models import Vip

SEX = (
        ('男', '男'),
        ('女', '女')
    )


class User(models.Model, ModelMixin):
    """
    手机号
    昵称
    性别
    出生日
    个人形象
    常居地
    """

    phonenum = models.CharField(max_length=32, verbose_name='手机号', unique=True)
    nickname = models.CharField(max_length=64, verbose_name='昵称', unique=True)
    gender = models.CharField(max_length=8, choices=SEX, verbose_name='性别', default='male')
    birthday = models.DateField(verbose_name='出生日', default='2000-1-1')
    avatar = models.CharField(max_length=256, verbose_name='个人头像的url地址')
    location = models.CharField(max_length=128, verbose_name='常居地')

    # vip和用户之间是一对多的关系, 把关系定义在多这一头,即用户
    vip_id = models.IntegerField(default=1, verbose_name='用户的vipid')

    @property
    def vip(self):
        # 返回用户的vip
        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    # 把profile变成user的属性
    # profile = Profile.objects.get(id=self.id)
    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            # 先从缓存中获取数据,如果获取不到,再从数据库获取,并写入缓存
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'<User {self.nickname} {self.phonenum}>'

    # def to_dict(self):
    #     return {
    #         'phonenum': self.phonenum,
    #         'nickname': self.nickname,
    #         'gender': self.gender,
    #         'birthday': str(self.birthday),
    #         'avatar': self.avatar,
    #         'location': self.location,
    #     }


class Profile(models.Model, ModelMixin):
    dating_location = models.CharField(max_length=128, verbose_name='目标城市')
    dating_gender = models.CharField(max_length=8, choices=SEX, verbose_name='匹配的性别')
    min_distance = models.IntegerField(default=0, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=50, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='不让陌生人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'profile'

