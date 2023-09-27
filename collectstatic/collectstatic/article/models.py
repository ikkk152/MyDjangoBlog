from django.db import models
from markdownx.models import MarkdownxField
from user.models import Users


class CreateDateModel(models.Model):
    create_datetime = models.DateTimeField('发布时间', auto_now_add=True)

    class Meta:
        abstract = True


class Article(CreateDateModel, models.Model):
    STATUS_CHOICE = (
        ('d', '草稿'),
        ('p', '发表')
    )
    user = models.ForeignKey(Users, verbose_name='用户', on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=30)
    # content = models.TextField('正文')
    content = MarkdownxField(verbose_name='正文')

    last_edit_datetime = models.DateTimeField('最近编辑', null=True, blank=True)
    views = models.PositiveIntegerField('浏览量', default=0)
    status = models.CharField('文章状态', choices=STATUS_CHOICE, max_length=1)

    class Meta:
        db_table = 'Article'
        ordering = ['create_datetime']
        verbose_name = '文章'
        verbose_name_plural = verbose_name

# class Tag(models.Model):
#     name = models.CharField('标签名', max_length=10)
#
#     class Meta:
#         db_table = 'Tag'
#         verbose_name = '标签'
#         verbose_name_plural = verbose_name
#
#
# class Comment(CreateDateModel, models.Model):
#     article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
#     user = models.ForeignKey(Users, verbose_name='用户', on_delete=models.CASCADE)
#     content = models.TextField()
#     parent = models.ForeignKey('self', verbose_name='父评论', on_delete=models.CASCADE, related_name='child')
#     reply = models.ForeignKey('self', verbose_name='父评论', on_delete=models.CASCADE, related_name='reply')
#
#     class Meta:
#         db_table = 'Comment'
#         verbose_name = '评论'
#         verbose_name_plural = verbose_name
#
#
# class ArticleLike(models.Model):
#     article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
#     user = models.ForeignKey(Users, verbose_name='用户', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'ArticleLike'
#         verbose_name = '文章点赞'
#         verbose_name_plural = verbose_name
#
#
# class CommentLike(models.Model):
#     comment = models.ForeignKey(Comment, verbose_name='文章', on_delete=models.CASCADE)
#     user = models.ForeignKey(Users, verbose_name='用户', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'CommentLike'
#         verbose_name = '评论点赞'
#         verbose_name_plural = verbose_name
#
#
# class UserRelation(models.Model):
#     pass
#
#
# class Message(models.Model):
#     pass
#
#
# class History(models.Model):
#     pass
