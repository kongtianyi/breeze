from django.db import models
from django.utils import timezone


class Articles(models.Model):
    id = models.IntegerField("ID", primary_key=True)
    title = models.TextField("文章标题")
    category_id = models.IntegerField("分类id")
    tags = models.TextField("标签")
    content = models.TextField("文章内容")
    summery = models.TextField("文章简介", null=True)
    pv = models.IntegerField("Page View", null=True, blank=True, default=0)
    uv = models.IntegerField("Unique View", null=True, blank=True, default=0)
    comment_count = models.IntegerField("评论数", null=True, blank=True, default=0)
    url = models.CharField("时间索引url", max_length=200, null=True, blank=True, default="")
    create_time = models.DateTimeField("创建时间", default=timezone.now)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def to_json_dict(self):
        self.create_time = self.create_time.strftime("%Y-%m-%d %H:%M")
        self.update_time = self.update_time.strftime("%Y-%m-%d %H:%M")
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        db_table = 'articles'


class Categorys(models.Model):
    id = models.IntegerField("ID", primary_key=True)
    category_name = models.CharField("分类名", max_length=100)
    parent_id = models.IntegerField("父分类id")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def to_json_dict(self):
        self.create_time = self.create_time.strftime("%Y-%m-%d %H:%M")
        self.update_time = self.update_time.strftime("%Y-%m-%d %H:%M")
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        db_table = 'categorys'


class Comments(models.Model):
    id = models.IntegerField("ID", primary_key=True)
    article_id = models.IntegerField("评论博文id")
    comment_author = models.CharField("评论者昵称", max_length=30)
    comment_author_email = models.CharField("评论者邮箱", max_length=100)
    comment_author_url = models.CharField("评论者主页", max_length=200)
    comment_author_ip = models.CharField("评论者ip", max_length=100)
    comment_content = models.TextField("评论内容")
    comment_approved = models.IntegerField("评论是否通过审核", null=True, blank=True, default=0)
    comment_parent = models.IntegerField("父评论id 0-文章评论")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def to_json_dict(self):
        self.create_time = self.create_time.strftime("%Y-%m-%d %H:%M")
        self.update_time = self.update_time.strftime("%Y-%m-%d %H:%M")
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        db_table = 'comments'


class Exts(models.Model):
    id = models.IntegerField("ID", primary_key=True)
    key = models.CharField("Key", max_length=50)
    value = models.CharField("Value", max_length=200, null=True, blank=True, default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def to_json_dict(self):
        self.create_time = self.create_time.strftime("%Y-%m-%d %H:%M")
        self.update_time = self.update_time.strftime("%Y-%m-%d %H:%M")
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        db_table = 'ext'
