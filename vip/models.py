from django.db import models


class Vip(models.Model):
    level = models.IntegerField(verbose_name='vip等级', default=0)
    price = models.FloatField(verbose_name='vip价格')
    name = models.CharField(verbose_name='vip名称', max_length=128)

    def __str__(self):
        return f'<Vip ({self.level})>'

    def has_perm(self, perm_name):
        # 判断vip是否具有某个权限
        # 先从关系表中取出当前vip所具有的所有权限
        relation = VipPermRelation.objects.filter(vip_id=self.id).only('perm_id')
        # 取出权限id
        perm_id_list = [perm.perm_id for perm in relation]
        # 根据权限id取出权限对象
        perms = Permission.objects.filter(id__in=perm_id_list)
        for perm in perms:
            if perm_name == perm.name:
                # 说明有权限
                return True
        return False


class Permission(models.Model):
    name = models.CharField(verbose_name='权限名称', max_length=64)
    description = models.TextField(verbose_name='权限描述')

    def __str__(self):
        return f'<Perm ({self.name})>'


class VipPermRelation(models.Model):
    # vip和权限的关系表
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()
