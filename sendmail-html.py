# -*- coding: utf-8 -*-
import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

if __name__ == '__main__':

    subject, from_email, to = '来自www.foxchan.com的测试邮件', 'chenlei@emar.com', '314969569@qq.com'
    text_content = '欢迎访问www.foxchan.com，这里是foxchan的站点，专注于Python和Django技术的分享！'
    html_content = '''
                   <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.foxchan.com</a>，
                   这里是foxchan站点，专注于Python和Django技术的分享！</p>
                   <p>请点击站点链接完成注册确认！</p>
                   <p>此链接有效期为{}天！</p>
                   '''.format('101.254.242.12:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
