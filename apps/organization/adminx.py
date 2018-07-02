# -*-coding:utf-8-*-

__Author__ = "Mr.D"
__Date__ = '2018\4\6 0006 11:56'


import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    # model_icon = 'fa fas fa-building'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_num']
    search_fields = ['name', 'desc', 'click_num', 'fav_num']
    list_filter = ['name', 'desc', 'click_num', 'fav_num']
    # 下拉框变搜索
    relfield_style = 'fk-ajax'
    # 富文本插件
    style_fields = {"desc": "ueditor"}


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company']
    search_fields = ['org', 'name', 'work_year', 'work_company']
    list_filter = ['org__name', 'name', 'work_year', 'work_company']
    # model_icon = 'fa fas fa-chalkboard-teacher'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)