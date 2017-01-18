# coding=utf-8

from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import viewsets, status
from rest_framework.decorators import list_route, detail_route

from util.response import error_response, empty_response, json_response
from util.schema import get_object_or_400
from ins.serializer import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = User.USERNAME_FIELD

    @list_route(methods=['post'])
    def login(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
        else:
            return error_response('Login fail', status=status.HTTP_401_UNAUTHORIZED)
        return empty_response()

    @detail_route(methods=['get'])
    def followers(self, request, name):
        user = get_object_or_400(User, name=name)
        followers = User.objects.get_followers(user)
        resp = [{'avatar': user.avatar, 'name': user.name} for user in followers]
        page = self.paginate_queryset(resp)
        if page is not None:
            return self.get_paginated_response(page)
        return json_response(page)

    @detail_route(methods=['get'])
    def following(self, request, name):
        user = get_object_or_400(User, name=name)
        following = User.objects.get_following(user)
        resp = [{'avatar': user.avatar, 'name': user.name} for user in following]
        page = self.paginate_queryset(resp)
        if page is not None:
            return self.get_paginated_response(page)
        return json_response(page)

    @detail_route(methods=['get'])
    def ins(self, request, name):
        user = get_object_or_400(User, name=name)
        ins = User.objects.get_ins(user)
        resp = [{'content': item.content} for item in ins]
        page = self.paginate_queryset(resp)
        if page is not None:
            return self.get_paginated_response(page)
        return json_response(page)
