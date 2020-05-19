from django.db import models


class Swiped(models.Model):
    # 可以把滑动操作,抽象成一个模型
    # 用一个模型精确的表示用户的滑动操作即可.
    # 一个滑动操作会有被滑的人的id, 滑动人的id.滑动的类型, 滑动的时间点.
    MARK = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('superlike', 'superlike')
    )
    uid = models.IntegerField(verbose_name='用户自身的id')
    sid = models.IntegerField(verbose_name='被滑动人的id')
    mark = models.CharField(choices=MARK, verbose_name='滑动类型', max_length=16)
    time = models.DateTimeField(verbose_name='滑动时间', auto_now_add=True)
