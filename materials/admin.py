from django.contrib import admin

from materials.models import Course, Lesson, Subscribe


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course",)
