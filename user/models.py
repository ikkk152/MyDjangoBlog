from django import db
from django.contrib.auth.models import AbstractUser
from django.db import models


class FixField(models.Field):
    def db_type(self, connection):
        return 'char(%s)' % self.max_length


# Create your models here.
class Users(AbstractUser):
    email = models.EmailField('邮箱地址', unique=True)  # email唯一
    username = models.CharField('昵称', max_length=20)
    phone = FixField('手机号', max_length=11, null=True, blank=True, unique=True)
    avatar = models.ImageField('用户头像', upload_to='avatars/', null=True, blank=True)
    biography = models.CharField('个人简介', max_length=150, null=True, blank=True)
    USERNAME_FIELD = 'email'  # 使用 email 作为登录字段
    REQUIRED_FIELDS = []  # 设置注册时必须填写的字段，username 从此列表中移除，因为已经使用 email 替代

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
