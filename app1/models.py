from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 20)
    email = models.EmailField()
    created_time = models.CharField(max_length = 50,default=now)
    comment_num = models.PositiveIntegerField(verbose_name='评论数',default=0)
    avatar = models.ImageField(upload_to = 'media',default='media/default.png')

    def __str__(self):
        return self.username

    def comment(self):
        self.comment_num += 1
        self.save(update_fields=['comment_num'])

    def comment_del(self):
        self.comment_num -= 1
        self.save(update_fields=['comment_num'])


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email')

class Category(models.Model):
    name = models.CharField(verbose_name="类别名称", max_length=64)

    def __str__(self):
        return self.name

class Blog(models.Model):
    blog_id = models.AutoField(primary_key = True)
    title = models.CharField(verbose_name="标题", max_length=100)
    content = models.TextField(verbose_name="内容", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=now)
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment_num = models.PositiveIntegerField(verbose_name='评论数',default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    body = models.TextField()
    createtime = models.DateTimeField(verbose_name="创建时间", default=now)
    article = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-createtime'] #查询数据时，自动排序


