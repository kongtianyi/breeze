# -*- coding: utf-8 -*-

from django.db.models import F
from blog.models import Exts


def add_blog_pv_uv(func):
    '''
    增加博客维度的pv和uv
    '''
    def _add_user_pv_uv(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if "blog_viewed" not in request.COOKIES:
            response.set_cookie("blog_viewed", "1")
            Exts.objects.filter(key="uv").update(value=F("value") + 1)
        Exts.objects.filter(key="pv").update(value=F("value") + 1)
        return response
    return _add_user_pv_uv
