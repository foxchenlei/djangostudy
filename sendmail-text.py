# -*- coding: utf-8 -*- 
import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

if __name__ == '__main__':   

    send_mail(
        '来自foxchan的测试邮件',
        '欢迎访问foxchan的blog',
        'chenlei@emar.com',
        ['314969569@qq.com'],
    )
