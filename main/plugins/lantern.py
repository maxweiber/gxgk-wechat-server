#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
from .. import app, celery
from . import wechat_custom
from ..models.user import User

@celery.task
def gress_lantern_riddles(openid, text):
    user_info = User.query.filter_by(openid=openid).first()

    url = 'http://lantern.gxgk.cc/?s=/Home/Riddle/index'

    payload = {"key":app.config['LANTERN_KEY'],
               "openid":openid,"nickname":user_info.nickname,"msg":text}
    try:
        r = requests.post(url, data = payload, timeout=20)
    except Exception, e:
        app.logger.warning(u"lantern 请求或解析失败: %s, text: %s" % (e, text))
        return wechat_custom.send_text(openid, u'小喵犯傻了，请重新回复！')
    else:
        try:
            answer = r.json()['response']
        except Exception, e:
            app.logger.warning(u"lantern 解析Json失败: %s, text: %s context: %s" % (e, text, r.text))
        else:
            return wechat_custom.send_text(openid, answer)



def before_lantern_riddles(openid, text):
    user_info = User.query.filter_by(openid=openid).first()

    url = 'http://lantern.gxgk.cc/?s=/Home/Riddle/riddlebegin'

    payload = {"key":app.config['LANTERN_KEY'],
               "openid":openid,"nickname":user_info.nickname,"msg":text}
    try:
        r = requests.post(url, data = payload, timeout=20)
    except Exception, e:
        app.logger.warning(u"before_lantern 请求或解析失败: %s, text: %s" % (e, text))
        return wechat_custom.send_text(openid, u'小喵犯傻了，请重新回复！')
    else:
        try:
            order = r.json()['order']
        except Exception, e:
            app.logger.warning(u"before_lantern 解析Json失败: %s, text: %s context: %s" % (e, text, r.text))
        else:
            answer = r.json()['response']
            wechat_custom.send_text(openid, answer)
            if order != 'noenter':
                return None
            return 'noenter'