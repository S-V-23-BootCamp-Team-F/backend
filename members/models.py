from django.db import models

# Create your models here.
from django.db import models
from django import forms

# Create your models here.
class Member(models.Model):
    email = models.EmailField(max_length=100, verbose_name="사용자 이메일")
    password = models.CharField(verbose_name="사용자 비밀번호",max_length=100)
    user_status = models.BooleanField(default=True, verbose_name="사용자 상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="사용자 생성일")
    
    def __str__(self):
        return f'{self.email}'