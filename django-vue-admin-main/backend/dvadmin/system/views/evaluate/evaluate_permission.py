# -*- coding: utf-8 -*-            
# @Time : 2023/10/23 20:15
#  :name
# @FileName: evaluate_permission.py
# @Software: PyCharm
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class Evaluate_permission(BasePermission):

    def has_object_permission(self, request, view, obj):
        api = request.path  # 当前请求接口
        print(api)
        if request.user.is_superuser == 1:
            return True
        else:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return obj.creator == request.user