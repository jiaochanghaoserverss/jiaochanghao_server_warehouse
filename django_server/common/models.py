from django.db import models
from common.fields import SimpleForeignKey


class BaseQueryset(models.QuerySet):

    def delete(self):
        # 标记删除
        self.update(deleted=True)

    def remove(self):
        # 真删
        super().delete()

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except:
            return None


class BaseManager(models.manager.BaseManager.from_queryset(BaseQueryset), models.Manager):
    def get_queryset(self):
        # 只获取没有被删除的内容
        return super(BaseManager, self).get_queryset().filter(deleted=False)

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except:
            return None


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间')
    deleted = models.BooleanField(default=False, help_text='是否删除')

    objects = BaseManager()
    raw_objects = models.Manager()

    class Meta:
        abstract = True

    @classmethod
    def update_exclude_fields(cls):
        return ['create_time', 'update_time']

    @classmethod
    def json_fields(cls):
        return '__all__'

    def delete(self, *args, **kwargs):
        assert self.pk is not None, (
            "%s object can't be deleted because its %s attribute is set to None." %
            (self._meta.object_name, self._meta.pk.attname)
        )
        self.deleted = True
        self.save()
