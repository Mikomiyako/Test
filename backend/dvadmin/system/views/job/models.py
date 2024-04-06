from django.db import models

# Create your models here.
from dvadmin.system.models import Dept
from dvadmin.utils.models import table_prefix, CoreModel
from rest_framework import serializers


class Job(CoreModel):
    job_name = models.CharField(max_length=40, verbose_name="工作名称", help_text="工作名称")
    job_address = models.CharField(max_length=40, verbose_name="工作地点", help_text="工作地点")

    job_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="工作时间", verbose_name="工作时间")
    # job_type = models.CharField(max_length=40, verbose_name="工作类型", help_text="工作类型")
    duration = models.CharField(max_length=40, verbose_name="工期", help_text="工期")
    wage = models.CharField(max_length=40, verbose_name="工资", help_text="工资")
    job_demand = models.CharField(max_length=40, verbose_name="工作要求", help_text="工作要求", null=True)
    job_best_offer = models.CharField(max_length=100, verbose_name="最优报价", help_text="最优报价", null=True)
    GENDER_CHOICES = (
        (0, "木工作业"),
        (1, "砌筑作业"),
        (2, "抹灰作业"),
        (3, "油漆作业"),
        (4, "脚手架作业"),
        (5, "焊接作业")
    )
    job_type = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="工作类型", null=True, blank=True, help_text="性别"
    )

    dept = models.ForeignKey(
        to=Dept,
        verbose_name="所属部门",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="关联部门",
    )

    class Meta:
        db_table = table_prefix + "company_job"
        verbose_name = "公司_工作表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def to_dict(self):
        return {
            'id': self.id,
            'job_name': self.job_name,
            'job_address': self.job_address,
            'job_datetime': self.job_datetime.strftime("%Y-%m-%d %H:%M:%S") if self.job_datetime else None,
            'duration': self.duration,
            'wage': self.wage,
            'job_demand': self.job_demand,
            'job_type': self.get_job_type_display(),  # 使用 get_<field_name>_display() 来获取选择字段的可读值
            'commendation_index': self.commendation_index,
            'description': self.description,
            'update_datetime': self.update_datetime,
            'create_datetime': self.create_datetime,
            'dept_name': self.dept_name

        }
