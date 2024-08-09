from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import valid_link


class LessonSerializer(serializers.ModelSerializer):
    link = serializers.URLField(validators=[valid_link])

    class Meta:
        model = Lesson
        fields = ('__all__')


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('__all__')
