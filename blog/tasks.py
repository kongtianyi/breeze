from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_mail_task(recipient, from_user, to_user, article_title, article_url, old_comment, new_comment, old_comment_id):
    """
    发送收到新评论邮件
    :param recipient: 收到这封邮件的邮箱
    :param from_user: 评论者
    :param to_user: 被评论者
    :param article_title: 评论所属文章标题
    :param article_url: 评论所属文章url
    :param old_comment: 原评论
    :param new_comment: 新评论
    :param old_comment_id: 原评论id
    :return:
    """
    msg = """
        <p>%s你好，你在<a href="http://kongtianyi.cn">孔天逸'Blog</a>><a href="http://kongtianyi.cn/%s">%s</a>的评论有新回复了，<a href="http://kongtianyi.cn/%s#comments_id_%s">点此查看</a>。</p>
        <p>你的评论：%s</p>
        <p>%s的回复：%s</p>
        <strong>本邮件为系统后台自动发出，请勿直接回复。</strong>
    """ % (to_user, article_url, article_title, article_url, old_comment_id, old_comment, from_user, new_comment)
    try:
        send_mail('评论回复', '', settings.EMAIL_FROM, [recipient, ], html_message=msg)
    except Exception as e:
        pass
        # logging.error("When sent retrieve email, error %s occurred." % (e.__class__,))
