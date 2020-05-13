from django.db import models


class User(models.Model):
    """
    手机号
    昵称
    性别
    出生日
    个人形象
    常居地
    """
    SEX = (
        ('男', '男'),
        ('女', '女')
    )
    phonenum = models.CharField(max_length=32, verbose_name='手机号', unique=True)
    nickname = models.CharField(max_length=64, verbose_name='昵称', unique=True)
    gender = models.CharField(max_length=8, choices=SEX, verbose_name='性别', default='male')
    birthday = models.DateField(verbose_name='出生日', default='2000-1-1')
    avatar = models.CharField(max_length=256, verbose_name='个人头像的url地址')
    location = models.CharField(max_length=128, verbose_name='常居地')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'<User {self.nickname} {self.phonenum}>'

    def to_dict(self):
        return {
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location,
        }
