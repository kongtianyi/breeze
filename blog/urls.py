from django.conf.urls import url
from . import views

urlpatterns = [
    # 展示型页面
    url(r'^$', views.index, name='index'),
    url(r'^page/(?P<page_num>[0-9]+)$', views.index, name='page'),
    url(r'^categories/(?P<category_name>([^/]*?)+)$', views.category_view, name='category_view'),
    url(r'^categories/(?P<category_name>([^/]*?)+)/page/(?P<page_num>[0-9]*)$', views.category_view, name='category_view_page'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<short_name>(.*?)+)$', views.article, name='article'),

    # restful API
    url(r'^comments$', views.comments, name='comments'),

    # 功能型页面
    url(r'^add_article$', views.add_article, name='add_article'),
    url(r'^add_comment', views.add_comment, name='add_comment')
]