from django.shortcuts import render
from django.views.generic.base import View
from .models import Course, CourseResource
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite,  CourseComments, UserCourse
from django.http import HttpResponse
import json
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q

# Create your views here.


class CourseListView(View):
    """
      课程机构列表功能
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 公开课搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)
                                             | Q(desc__icontains=search_keywords)
                                             | Q(detail__icontains=search_keywords)
                                             )

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
        try:
            page = request.GET.get('page', '1')
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, "course-list.html",
                      {
                          'all_courses': courses,
                          'sort': sort,
                          'hot_courses': hot_courses
                      })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        tag = course.tag

        # 获取相同标签的其他课程
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[0:1]
            # 如果选出来的是本课程则换第二个
            if relate_courses[0].name == course.name:
                relate_courses = Course.objects.filter(tag=tag)[1:2]

        else:
            relate_courses = []

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        }
                      )


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        # 查询用户是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        # 获取学过该课的所有同学的ID
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取所有学过该课的同学所学过的课程的ID
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resources,
            'relate_courses': relate_courses,
        }
                      )


class CommentView(LoginRequiredMixin, View):
    """
    课程评论页显示
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()

        user_courses = UserCourse.objects.filter(course=course)

        # 获取学过该课的所有同学的ID
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 获取所有学过该课的同学所学过的课程的ID
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses,

        }
                      )


class AddCommentView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')


