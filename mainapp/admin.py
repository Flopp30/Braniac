from django.contrib import admin
from mainapp.models import News, Courses, CourseTeachers, Lesson

admin.site.register(Courses)
admin.site.register(CourseTeachers)
admin.site.register(Lesson)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body', 'created', 'updated')
