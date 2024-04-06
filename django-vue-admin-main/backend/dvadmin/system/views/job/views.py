# Create your views here.
# Job/views.py
# Create your views here.
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from dvadmin.system.views.evaluate.models import Evaluate
from dvadmin.system.views.job.recommend import recommend_content, recommend_mark
from dvadmin.utils.filters import DataLevelPermissionsFilter
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.system.views.job.models import Job
from rest_framework.decorators import action


class JobSerializer(CustomModelSerializer):
    """
    序列化器
    """
    dept_name = serializers.CharField(source='dept.name', read_only=True)
    # dept = DeptSerializer()
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["id"]


class JobCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = Job
        fields = '__all__'
# 以上是序列化函数，可以使用新建一个serializers.py来进行管理

class JobCreateSerializer(CustomModelSerializer):
    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept_id = data.dept_belong_id
        # 获取相同类型的所有工作，除去当前这一条
        job_list = Job.objects.filter(job_type=data.job_type).exclude(id=data.id)
        if len(job_list) > 0:
            # 计算同一种类的工作的工期
            durations = [obj.duration for obj in job_list]
            # 计算同一种类的工作的工资
            wages = [obj.wage for obj in job_list]

            durations_sum = sum(int(value) for value in durations)
            wages_sum = sum(int(value) for value in wages)
            average = wages_sum // durations_sum
            data.job_best_offer = average * int(data.duration)
        else:
            # 最优报价默认值。

            data.wages = [obj.wage for obj in job_list]
            data.job_best_offer = 3000
        data.save()
        return data

    class Meta:
        model = Job
        fields = '__all__'

class JobViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    create_serializer_class = JobCreateSerializer


    extra_filter_backends = [DataLevelPermissionsFilter]
    permission_classes = []
    search_fields = ['label']

    # 推荐工作
    @action(methods=["GET"], detail=False)
    def recommend_job(self, request):
        """获取当前用户信息"""
        skill = request.user.skill
        user_job_title = request.user.job_title
        if skill is None or skill.strip() == "" or user_job_title is None or user_job_title.strip() == "":
            return ErrorResponse(msg="工人用户需先完成<拥有技能>和<目标工作>信息的填写，请前往个人信息中填写，以下内容展示已发布的工作")
        # 获取用户已有的工作评分数量,工人评分数据少时，用recommend_mark协同过滤会得到相同的推荐指数，
        # 建议工作数据和评分数据多时recommend_mark，
        count = Evaluate.objects.filter(creator=request.user.id).count()
        # 当前用户已经有工作对应的评分
        user_evaluate = Evaluate.objects.filter(mark__isnull=False, creator_id=request.user.id).count()
        if count >= 100 and user_evaluate >= 10:
            # 根据 用户-> 工作评分推荐工作
            return recommend_mark(request.user)
        else:
            # 基于内容推荐工作
            return recommend_content(request.user)


