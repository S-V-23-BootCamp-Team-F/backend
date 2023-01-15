from django.db import models

# Create your models here.
from django.db import models
from members.models import Member
# Create your models here.

class Disease(models.Model):
    name =models.CharField(verbose_name="질병 이름",max_length=100)
    cause = models.TextField(verbose_name="질병 원인")
    feature=models.TextField(verbose_name="병진")
    solution=models.TextField(verbose_name="방제 방법")
    created_at = models.DateTimeField(auto_created=True,verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="업데이트일")
    
    def __str__(self):
        return self.name

class Plant(models.Model):
    type = models.CharField(verbose_name="작물종류",max_length=100)
    explaination = models.CharField(verbose_name="작물 설명",max_length=1000)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

class Dignoisis(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease,on_delete=models.PROTECT)
    plant = models.ForeignKey(Plant,on_delete=models.PROTECT)
    type = models.CharField(verbose_name="식물 종류",max_length=10)
    picture = models.URLField(verbose_name="식물 사진",max_length=250)
    created_at = models.DateTimeField(verbose_name='생성일',auto_now_add=True)
    
    def __str__(self):
        return self.member,self.disease_code