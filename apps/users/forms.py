# -*-coding:utf-8-*-
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

__Author__ = "Mr.D"
__Date__ = '2018\4\7 0007 1:21'


# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 忘记密码提交表单
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    # 在前端显示验证码
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 修改密码提交表单
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']


# 用户头像修改表单
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']




