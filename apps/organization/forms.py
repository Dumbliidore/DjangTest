# -*-coding:utf-8-*-

__Author__ = "Mr.D"
__Date__ = '2018\4\14 0014 19:39'

from django import forms
from operation.models import UserAsk
import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = r'^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', 'mobile_invalid')