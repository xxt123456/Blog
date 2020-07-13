from django.db import models


# from django.db.models import BooleanField as _BooleanField
#
# # Create your models here.
# """
# 重写BooleanField方法
# """
# class BooleanField(_BooleanField):
#     def get_prep_value(self, value):
#         if value in ('0','false','False'):
#             return False
#         elif value in ('1','true','True'):
#             return True
#         else:
#             return super(BooleanField, self).get_prep_value(value)


class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(upload_to='./static/imgs/avatar', default='./static/imgs/avatar/default.png',
                               verbose_name='头像')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题',max_length=64)
    site = models.CharField(verbose_name='个人博客前缀',max_length=32,unique=True)
    theme = models.CharField(verbose_name='博客主题',max_length=32)
    user = models.OneToOneField(to='UserInfo',to_field='nid',on_delete=models.CASCADE)

class Category(models.Model):
    """
    个人文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题',max_length=32)
    blog = models.ForeignKey(verbose_name='属于博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

class ArticleDetail(models.Model):
    """
    文章详细
    """
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章',to='Article',to_field='nid',on_delete=models.CASCADE)

class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='nid',on_delete=models.CASCADE)
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)

class Article(models.Model):
    """
        文章
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题',max_length=128)
    summary = models.CharField(verbose_name='文章简介',max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    creat_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    article_img = models.ImageField(upload_to='./static/img/art_imgs/', verbose_name='主题照片', default=None)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='文章类型',to='Category',to_field='nid',on_delete=models.CASCADE)

    type_choices = [
        (1,'Python'),
        (2,'Linux'),
        (3,'C++'),
        (4,"架构师"),
    ]
    article_type_id = models.IntegerField(choices=type_choices,default=None)

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid',on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid',on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

# class UserMessage(models.Model):
#     """
#     信息通知
#     """


class Proxy_Pool(models.Model):
    ip = models.CharField(verbose_name='ip', max_length=32)
    port = models.IntegerField(verbose_name='端口')
    protcol = models.CharField(verbose_name='协议类型', max_length=32)
    location = models.CharField(verbose_name='代理归属地', max_length=32, blank=True)
    ip_respons = models.CharField(verbose_name='代理响应时间', max_length=32, blank=True)
    update = models.DateField(verbose_name='代理更新时间', max_length=64, auto_now_add=True)
