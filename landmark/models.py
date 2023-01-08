from django.db import models

# Create your models here.
from django.db import models
from members.models import Member
# Create your models here.
class Landmark(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    picture = models.URLField(verbose_name='이미지 URL',max_length=250, )
    latitude = models.FloatField(verbose_name='위도')
    longitude = models.FloatField(verbose_name='경도')
    name = models.CharField(verbose_name='랜드마크 이름',max_length=100)
    created_at = models.DateTimeField(verbose_name='생성일',auto_now_add=True)