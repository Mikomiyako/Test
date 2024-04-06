# Create your models here.
from django.db import models

from dvadmin.system.models import Users
from dvadmin.utils.models import CoreModel, table_prefix
from dvadmin.system.views.job.models import Job


class Evaluate(CoreModel):
    mark = models.IntegerField(null=True, verbose_name='评分', help_text="评分")
    GENDER_CHOICES = (
        (0, "接受工作"),
        (1, "完成工作"),
        (2, "取消工作")
    )
    evaluate_status = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="状态", null=True, blank=True, help_text="状态"
    )

    job = models.ForeignKey(
        to=Job,
        verbose_name="工作信息",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="关联工作",
    )



    class Meta:
        db_table = table_prefix + "job_evaluate"
        verbose_name = '工作工人评分表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
