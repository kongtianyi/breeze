from django.contrib import admin
from .models import Articles, Categorys, Comments, Exts


class ArticlesAdmin(admin.ModelAdmin):
    readonly_fields = ('update_time',)
    list_display = ('id', 'title', 'category_id', 'tags', 'pv', 'uv',
                    'comment_count', 'create_time', 'update_time')


class CategorysAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'create_time', 'update_time')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'article_id', 'comment_author_email',
                    'comment_author_url', 'comment_author_ip',
                    'comment_content', 'create_time', 'update_time')


class ExtAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value', 'create_time', 'update_time')

admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Categorys, CategorysAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Exts, ExtAdmin)

