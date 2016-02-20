#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from .. import app, celery
from . import wechat_custom
from ..models import get_user_nickname


@celery.task
def gress_lantern_riddles(openid, text):
    user_nickname = get_user_nickname(openid)

    url = 'http://lantern.gxgk.cc/?s=/Home/Riddle/index'

    payload = {"key": app.config['LANTERN_KEY'],
               "openid": openid, "nickname": user_nickname, "msg": text}
    try:
        r = requests.post(url, data=payload, timeout=20)
        answer = r.json()['response']
    except Exception, e:
        app.logger.warning(u"lantern 请求或解析失败: %s, text: %s" % (e, text))
        return wechat_custom.send_text(openid, u'小喵犯傻了，请重新回复！')
    else:
        return wechat_custom.send_text(openid, answer)


@celery.task
def before_lantern_riddles(openid, text):
    user_nickname = get_user_nickname(openid)

    url = 'http://lantern.gxgk.cc/?s=/Home/Riddle/riddlebegin'

    payload = {"key": app.config['LANTERN_KEY'],
               "openid": openid, "nickname": user_nickname, "msg": text}
    try:
        r = requests.post(url, data=payload, timeout=20)
        answer = r.json()['response']
    except Exception, e:
        app.logger.warning(u"before_lantern 请求或解析失败: %s, text: %s" % (e, text))
        return wechat_custom.send_text(openid, u'小喵犯傻了，请重新回复！')
    else:
        return wechat_custom.send_text(openid, answer)
