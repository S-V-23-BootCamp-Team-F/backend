from django.db import models
from members.models import Member

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
        return self.plant_type

class Diagnosis(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease,on_delete=models.PROTECT)
    plant = models.ForeignKey(Plant,on_delete=models.PROTECT)
    picture = models.URLField(verbose_name="식물 사진",default='',max_length=500)
    result_picture =models.URLField(verbose_name="판별 후 식물사진",default='',max_length=500)
    status = models.CharField(default="OK" ,max_length=10)
    created_at = models.DateTimeField(verbose_name='생성일',auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.disease