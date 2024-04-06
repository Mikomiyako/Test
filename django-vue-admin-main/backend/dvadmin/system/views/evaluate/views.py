# Create your views here.
# Evaluate/views.py
# Create your views here.
from rest_framework.decorators import action

from dvadmin.system.views.job.models import Job
from rest_framework import serializers
from dvadmin.utils.filters import DataLevelPermissionsFilter
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.permission import Evaluate_permission
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.system.views.evaluate.models import Evaluate

from dvadmin.system.views.job.views import JobSerializer


class EvaluateSerializer(CustomModelSerializer):
    """
    序列化器
    """
    job = JobSerializer(read_only=True)

    class Meta:
        model = Evaluate
        fields = "__all__"
        read_only_fields = ["id"]


class EvaluateCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = Evaluate
        fields = '__all__'
# 以上是序列化函数，可以使用新建一个serializers.py来进行管理

class EvaluateCreateSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        print(**kwargs)
        data = super().save(**kwargs)
        # data.dept_id = data.dept_belong_id
        # data.save()
        return data

    class Meta:
        model = Evaluate
        fields = '__all__'


class EvaluateViewSet(CustomModelViewSet):
    """
    书籍管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Evaluate.objects.all()
    serializer_class = EvaluateSerializer
    create_serializer_class = EvaluateCreateSerializer
    # extra_filter_backends = [DataLevelPermissionsFilter]
    extra_filter_backends = []
    permission_classes = []
    # permission_classes = [Evaluate_permission]
    search_fields = ['label']

    # @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    # def evaluate_info(self, request):
    #     return ""

    # 个人的劳务合同接口   只显示个人的劳务合同（投递过的工作）
    @action(methods=["GET"], detail=False, )
    def evaluate_user(self, request):
        """获取当前用户信息"""
        user = request.user

        user_dept_id = getattr(request.user, "dept_id", None)
        queryset = self.filter_queryset(self.get_queryset())
        if request.user.is_superuser == 0:
            queryset = queryset.filter(creator=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    # 企业劳务管理 -》 合同管理 接口
    # 查询公司发布的所有工作 对应的评价（投递过的个人发布的评价）
    @action(methods=["GET"], detail=False)
    def evaluate_company(self, request):
        """获取当前用户信息"""
        user = request.user
        queryset = self.filter_queryset(self.get_queryset())
        if request.user.is_superuser == 0:
            job_id_list = Job.objects.filter(dept=user.dept_id).values_list('id',flat=True)
            queryset = queryset.filter(job_id__in=job_id_list)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        for data in serializer.data:
            data['user.name'] = serializers.CharField(read_only=True, source='user.name')
        return SuccessResponse(data=serializer.data, msg="获取成功")
