from django.contrib import admin
from mainapp.models import News, Courses, CourseTeachers, Lesson, CourseFeedback
from django.utils.html import format_html


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'link_', 'body', 'created', 'updated')
    list_filter = ('deleted', 'created')
    ordering = ('-pk', 'deleted', 'created')
    list_per_page = 20
    search_fields = ('title', 'body')
    actions = ('mark_as_delete', 'mark_as_active',)

    def link_(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            f'/news/{obj.pk}/detail/',
            obj.preambule,
        )

    link_.short_description = 'Ссылка на новость:'

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'

    def mark_as_active(self, request, queryset):
        queryset.update(deleted=False)

    mark_as_active.short_description = 'Снять пометку на удаление'


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'link_', 'description', 'created', 'updated')
    list_filter = ('deleted', 'created')
    ordering = ('-pk', 'deleted', 'created')
    list_per_page = 20
    search_fields = ('name', 'description')
    actions = ('mark_as_delete', 'mark_as_active',)

    def link_(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            f'/courses/{obj.pk}',
            obj.name,
        )

    link_.short_description = 'Ссылка на курс:'

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'

    def mark_as_active(self, request, queryset):
        queryset.update(deleted=False)

    mark_as_active.short_description = 'Снять пометку на удаление'


@admin.register(CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_first', 'name_second', 'day_birth', 'deleted')
    list_filter = ('deleted',)
    ordering = ('-pk', 'name_second', 'deleted')
    list_per_page = 20
    search_fields = ('name_first', 'name_second')
    actions = ('mark_as_delete', 'mark_as_active',)

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'

    def mark_as_active(self, request, queryset):
        queryset.update(deleted=False)

    mark_as_active.short_description = 'Снять пометку на удаление'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'course', 'description', 'created', 'updated')
    list_filter = ('deleted', 'created')
    ordering = ('course', '-pk', 'deleted', 'created')
    list_per_page = 20
    search_fields = ('title', 'description', 'course')
    actions = ('mark_as_delete', 'mark_as_active',)

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'

    def mark_as_active(self, request, queryset):
        queryset.update(deleted=False)

    mark_as_active.short_description = 'Снять пометку на удаление'


@admin.register(CourseFeedback)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'link_', 'course',  'user', 'rating')
    list_filter = ('deleted', 'created', 'course')
    ordering = ('course', '-pk', 'user')
    list_per_page = 20
    search_fields = ('course', 'rating', 'course')
    actions = ('mark_as_delete', 'mark_as_active',)

    def link_(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            f'/courses/{obj.pk}',
            f'{obj.user}_{obj.course}',
        )

    link_.short_description = 'Ссылка на отзыв:'

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удаленным'

    def mark_as_active(self, request, queryset):
        queryset.update(deleted=False)

    mark_as_active.short_description = 'Снять пометку на удаление'
