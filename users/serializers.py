#!coding=utf-8
from .models import UserProfile
from rest_framework import serializers
from WechatAPI.Login import WXLogin
from django.conf import settings


class UserSerializer(serializers.HyperlinkedModelSerializer):
    code = serializers.CharField(max_length=255, required=False)

    def create(self, validated_data=None):
        if validated_data is None:
            validated_data = self.validated_data
        data = validated_data  # 创建副本
        code = data['code']
        wxlogin = WXLogin(settings.WX_APPID, settings.WX_SECRET)
        openid = wxlogin.login(code)['openid']
        try:
            user = UserProfile.objects.get(openid=openid)
            return user
        except UserProfile.DoesNotExist:
            data['openid'] = openid
            del data['code']  # 将Code变为OpenID
            return UserProfile.objects.create(**data)

    def update(self, instance, validated_data=None):
        for attr, value in validated_data.items():
            if attr != "code" or attr != "openid":
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ['code', 'nickName', 'avatarUrl', 'description', 'school', 'grade']
