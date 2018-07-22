from django.db.models import F
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from blog.models import Articles, Categorys, Comments, Exts
from blog.decorators import add_blog_pv_uv
import datetime
import math
import json


@add_blog_pv_uv
def index(request, page_num=None):
    """
    博客主页面
    """
    # 第几页
    if not page_num:
        page_num = 1
    page_num = int(page_num)
    try:
        articlelist = Articles.objects.all().order_by('-create_time')[(page_num-1)*10: (page_num-1)*10+10]
    except AssertionError:
        raise Http404()
    # 分页板
    article_num = Articles.objects.count()
    # 调整标签格式，便于前端显示
    for article in articlelist:
        article.tags = article.tags.split(",")

    context = {
        "data": articlelist,
        "pages": [x+1 for x in range(0, math.ceil(article_num / 10))],
        "now_page": page_num,
        "categorys": get_categorys(),
        "blog_param": get_blog_param(),
    }
    return render(request, 'blog/index.html', context=context)


@add_blog_pv_uv
def category_view(request, category_name=None, page_num=None):
    """
    文章分类页面，模板与主页一致
    """
    # 第几页
    if not page_num:
        page_num = 1
    page_num = int(page_num)

    category_id = Categorys.objects.filter(category_name=category_name)[0].id

    try:
        articlelist = Articles.objects.filter(category_id=category_id).order_by("-create_time")[(page_num-1)*10: (page_num-1)*10+10]
    except AssertionError:
        raise Http404()
    # 分页板
    article_num = Articles.objects.filter(category_id=category_id).count()
    # 调整标签格式，便于前端显示
    for article in articlelist:
        article.tags = article.tags.split(",")

    context = {
        "data": articlelist,
        "pages": [x+1 for x in range(0, int(article_num / 10)+1)],
        "now_page": page_num,
        "categorys": get_categorys(),
        "blog_param": get_blog_param(),
    }
    return render(request, 'blog/index.html', context=context)


@add_blog_pv_uv
def article(request, year, month, day, short_name):
    """
    文章页
    """
    url = year + "/" + month + "/" + day + "/" + short_name
    art = Articles.objects.get(url=url)
    art.tags = art.tags.split(",")
    art_id = int(art.id)

    # 查出来上一篇和下一篇的url，不能根据id来索引是因为，上一个或下一个id并不一定挨着，可能已经被删了
    pre_art = Articles.objects.filter(id__lt=art_id)[0: 1]
    if pre_art:
        pre_art = pre_art[0].url
    else:
        pre_art = None
    next_art = Articles.objects.filter(id__gt=art_id)[0: 1]
    if next_art:
        next_art = next_art[0].url
    else:
        next_art = None

    context = {
        "data": art,
        "pre_art": pre_art,
        "next_art": next_art,
        "categorys": get_categorys(),
        "blog_param": get_blog_param(),
    }
    response = render(request, 'blog/article.html', context=context)

    # 增加pv和uv
    if "articles_viewed" in request.COOKIES:
        av = request.COOKIES["articles_viewed"].split(",")
        if str(art_id) in av:
            Articles.objects.filter(id=art_id).update(pv=F("pv") + 1)
        else:
            av.append(str(art_id))
            response.set_cookie("articles_viewed", ",".join(av))
            Articles.objects.filter(id=art_id).update(uv=F("uv") + 1, pv=F("pv") + 1)
    else:
        response.set_cookie("articles_viewed", str(art_id))
        Articles.objects.filter(id=art_id).update(uv=F("uv") + 1, pv=F("pv") + 1)

    return response


def comments(request):
    """
    获取评论的rest接口
    """
    if request.method != "GET":
        return HttpResponse(json.dumps({
                "status": "error",
                "message": "请求方式错误"
            }), content_type="application/json;charset=utf-8")
    article_id = request.GET.get("article_id")
    comment_approved = request.GET.get("comment_approved")
    
    # 侧边栏显示最近3条,姑且先这么写吧
    last = request.GET.get("last")
    if last:
        comments = Comments.objects.filter(comment_approved=1).order_by("-create_time")[:3]
        data = list()
        for comment in comments:
            comment_dict = comment.to_json_dict()
            art_id = int(comment_dict['article_id'])
            art = Articles.objects.filter(id=art_id)[0]
            comment_dict["article_url"] = art.url
            comment_dict["article_title"] = art.title
            comment = data.append(comment_dict)
        return HttpResponse(json.dumps({
            "status": "success",
            "message": "请求成功",
            "data": data
        }), content_type="application/json;charset=utf-8")

    if comment_approved is None or comment_approved == "":
        comment_approved = 1
    comments = Comments.objects.filter(article_id=article_id, comment_approved=comment_approved)
    data = list()
    for comment in comments:
        comment = data.append(comment.to_json_dict())
    return HttpResponse(json.dumps({
            "status": "success",
            "message": "请求成功",
            "data": data
        }), content_type="application/json;charset=utf-8")


@csrf_exempt
def add_article(request):
    """
    添加文章的rest接口
    """
    if request.method == "GET":
        return render(request, 'blog/form.html')
    elif request.method == "POST":
        title = request.POST.get("title")
        short_name = request.POST.get("short_name")
        category_id = int(request.POST.get("category_id"))
        tags = request.POST.get("tags")
        content = request.POST.get("content")
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        url = str(year) + "/" + str(month) + "/" + str(day) + "/" + short_name
        obj = Articles.objects.create(title=title, url=url,
                                      category_id=category_id, tags=tags, content=content)
        if not obj:
            result = json.dumps({
                "status": "error",
                "message": "添加文章失败:-("
            }, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json;charset=utf-8")
        result = json.dumps({
            "status": "success",
            "message": "添加文章成功:-)"
        }, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json;charset=utf-8")
    else:
        return Http404()


@csrf_exempt
def add_comment(request):
    """
    添加评论
    """
    if request.method != "POST":
        return HttpResponse("君子何不坦诚相见？")
    article_id = request.POST.get("article_id")
    comment_author = request.POST.get("author")
    comment_author_email = request.POST.get("email")
    comment_author_url = request.POST.get("url")
    comment_author_ip = get_client_ip(request)
    comment_content = request.POST.get("content")
    comment_parent = request.POST.get("comment_parent")
    if article_id is None or comment_author is None or comment_author_email is None \
        or comment_author_url is None or comment_content is None or comment_parent is None \
        or article_id == "" or comment_author == "" or comment_author_email == "" \
        or comment_author_url == "" or comment_content == "" or comment_parent == "":
        return HttpResponse("君子何不坦诚相见？")
    if str(comment_author).lower().find("script") != -1 or str(comment_author_email).lower().find("script") != -1 \
        or str(comment_author_url).lower().find("script") != -1 or str(comment_content).lower().find("script") != -1:
        return HttpResponse(json.dumps({
            "status": "error",
            "message": "不知小可与阁下有何过节，何故横施加害？！"
        }), content_type="application/json")
    Comments.objects.create(article_id=int(article_id), comment_author=comment_author,
                            comment_author_email=comment_author_email, comment_author_url=comment_author_url,
                            comment_author_ip=comment_author_ip, comment_content=comment_content,
                            comment_approved=1, comment_parent=comment_parent)
    # 给文章加上一个评论数
    if Articles.objects.filter(article_id=int(article_id)).update(comment_count=F("comment_count")+1) < 1:
        # todo log
        pass
    return HttpResponse(json.dumps({
        "status": "success",
        "message": "添加评论成功"
    }), content_type="application/json")


# 下面是一些供上边路由函数调用的一些封装函数
def get_categorys():
    """
    获取分类列表
    """
    categories = Categorys.objects.all()
    category_list = list()
    for category in categories:
        category = category.to_json_dict()
        count = Articles.objects.filter(category_id=category["id"]).count()
        category["count"] = count
        category_list.append(category)
    return category_list


def get_client_ip(request):
    """
    获取访问者IP
    """
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip


def get_blog_param():
    """
    获取博客基础参数
    """
    blog_param = dict()
    exts = Exts.objects.all()
    for ext in exts:
        if "friend_links" == ext.key:
            ext.value = eval(ext.value)
        blog_param[ext.key] = ext.value
    return blog_param

