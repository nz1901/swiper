import random

from django.core.cache import cache
from django.db import models
from django.db.models import query

from common import keys


def get(self, *args, **kwargs):
    # 根据最常用的查询去缓存.
    # 根据id和pk去查询的操作,我们做个缓存
    pk = kwargs.get('id') or kwargs.get('pk')

    if pk is not None:
        # 执行缓存操作
        # 先从缓存中拿
        key = keys.OBJECT % (self.model.__name__, pk)
        obj = cache.get(key)
        if obj is None:
            # 从数据库拿
            obj = self._get(*args, **kwargs)
            print('get object from database')
            # 存入缓存
            cache.set(key, obj, 86400 * 14 * (random.random()))
        return obj
    else:
        # 说明不是根据id和pk查找的, 不做缓存.
        # 需要调用原始的get方法.
        return self._get(*args, **kwargs)


def get_or_create(self, defaults=None, **kwargs):
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk is not None:
        # 执行缓存操作
        # 先从缓存中拿
        key = keys.OBJECT % (self.model.__name__, pk)
        obj = cache.get(key)
        if obj is None:
            # 从数据库拿
            obj = self._get_or_create(defaults=None, **kwargs)
            print('get or create object from database')
            # 存入缓存
            cache.set(key, obj, 86400 * 14 * (random.random()))
        return obj
    else:
        # 说明不是根据id和pk查找的, 不做缓存.
        return self._get_or_create(defaults=None, **kwargs)


def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

    self.full_clean(validate_unique=True)
    # 先调用原始的save方法.
    self._save(force_insert, force_update, using, update_fields)
    # 更新缓存中的数据
    key = keys.OBJECT % (self.__class__.__name__, self.pk)
    cache.set(key, self, 86400 * 14 * (random.random()))


def update(self, **kwargs):
    # 先调用原始的update方法
    result = self.ori_update(**kwargs)
    print(result)
    print(type(result))
    # 更新缓存中的数据
    print(f'{self.model.__name__} 更新缓存...')
    print(self.model)
    print(type(self.model))
    print(self.model.pk)
    instance = self.model()
    key = keys.OBJECT % (self.model.__name__, getattr(self.model, 'pk'))
    # 注意要更新的是model,不是queryset对象
    cache.set(key, self.model, 86400 * 14 * (random.random()))
    return result


# 动态的给Model添加了具有缓存功能的方法.这种做法叫做猴子补丁.
def model_patch():
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    query.QuerySet._get_or_create = query.QuerySet.get_or_create
    query.QuerySet.get_or_create = get_or_create

    # query.QuerySet.ori_update = query.QuerySet.update
    # query.QuerySet.update = update

    models.Model._save = models.Model.save
    models.Model.save = save


from django.core.cache.backends import locmem
from redis import Redis
