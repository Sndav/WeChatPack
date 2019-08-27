#!coding=utf8
from django.contrib.auth.backends import ModelBackend
from .models import *
from WechatAPI.Login import WXLogin
from django.conf import settings
from datetime import datetime
from rest_framework_jwt.settings import api_settings


class UserBackend(ModelBackend):
    def authenticate(self, username=None, password=None, code=None, openid=None, **kwargs):
        """
        :param username: 用于admin登陆
        :param password: 用于admin登陆
        :param code: WX Code
        :param openid WX openid
        :param kwargs:
        :return:
        """
        try:
            if username:
                user = UserProfile.objects.get(username=username)
                print(password)
                if not user.check_password(password):
                    user = None
            elif openid:  # 优先检测OpenID
                user = UserProfile.objects.get(openid=openid)
            elif code:  # 如果存在Code
                wxlogin = WXLogin(settings.WX_APPID, settings.WX_SECRET)  # 获取OpenID
                openid = wxlogin.login(code)['openid']
                try:
                    user = UserProfile.objects.get(openid=openid)
                except Exception as e:
                    user = None
            else:
                user = None
        except Exception as e:
            user = None
        return user


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'openid': user.openid
    }


def jwt_payload_handler(user):

    payload = {
        'openid': user.openid,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    return payload


def jwt_get_username_from_payload(payload):
    openid = payload.get('openid')
    return openid

