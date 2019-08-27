#!coding=utf8
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        code = request.data.get("code")
        user = authenticate(code=code)
        if user:
            login(request, user)
            jwt = jwt_encode_handler(jwt_payload_handler(user))
            return Response({'token': jwt})
        return Response({"error_code": 401, "error": "登陆失败"})

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            jwt = jwt_encode_handler(jwt_payload_handler(user))
            resp = {
                "token": jwt
            }
            return Response(resp)
        return Response({"error_code": 401, "error": "注册失败"})


class UserUpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def update(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)

        serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            ret = {
                "error_code": 0,
                "data": serializer.data
            }
            return Response(ret)
        return Response(
            {
                "error_code": 1,
                "error": serializer.errors,
                "data": serializer.data
            }
        )
