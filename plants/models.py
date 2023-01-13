from django.db import models
from members.models import Member

class Disease(models.Model):
    disease_code = models.CharField(verbose_name="질병 코드",max_length=10)
    name =models.CharField(verbose_name="질병 이름",max_length=100)
    cause = models.TextField(verbose_name="질병 원인")
    feature=models.TextField(verbose_name="병진")
    solution=models.TextField(verbose_name="방제 방법")
    
    def __str__(self):
        return self.disease_code
    
class Plant(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease,on_delete=models.PROTECT)
    type = models.CharField(verbose_name="식물 종류",max_length=10)
    picture = models.URLField(verbose_name="식물 사진",max_length=250)
    created_at = models.DateTimeField(verbose_name='생성일',auto_now_add=True)
    
    def __str__(self):
        return self.member,self.disease_code