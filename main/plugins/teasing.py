#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from .. import app, celery
from . import wechat_custom
from ..models import get_user_nickname
from ..plugins.state import set_user_state

@celery.task
def teasing_start(openid, text):
	user_nickname = get_user_nickname(openid)
	url = 'http://zw.gxgk.cc/Home/Contribute'
	payload = {"key": app.config['TEASING_KEY'],
		"openid": openid, "nickname": user_nickname, "msg": text}

	try:
		r = requests.post(url, data=payload, timeout=20)
		content = r.json()['content']
	except Exception, e:
		app.logger.warning(u"teasing 请求或解析失败: %s, text: %s" % (e, text))
		return wechat_custom.send_text(openid, u'小喵犯傻了，请重新回复！')
	else:
		return wechat_custom.send_text(openid, content)

@celery.task		
def commiserate(openid, text):
	user_nickname = get_user_nickname(openid)

	url = 'http://zw.gxgk.cc/Home/Contribute/saveCommiserate'

	payload = {"key": app.config['TEASING_KEY'],
	"openid": openid, "nickname": user_nickname, "msg": text}
	try:
		r = requests.post(url, data=payload, timeout=20)
		content = r.json()['content']
		order = r.json()['order']

	except Exception, e:
		app.logger.warning(u"before_lantern 请求或解析失败: %s, text: %s" % (e, text))
		return wechat_custom.send_text(openid, u'小喵犯傻了，请重新回复！')
	else:
		if order == 'end':
			set_user_state(openid, 'default')
		return wechat_custom.send_text(openid, content)
