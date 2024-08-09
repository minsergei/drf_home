from rest_framework import serializers
from materials.models import Course, Lesson, Subscribe
from materials.validators import valid_link


class LessonSerializer(serializers.ModelSerializer):
    link = serializers.URLField(validators=[valid_link])

    class Meta:
        model = Lesson
        fields = ('__all__')


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribe = serializers.SerializerMethodField()

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribe(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if Subscribe.objects.filter(user=user, course=obj).exists():
                return 'Подписан на курс'
            return 'Не подписан на курс'
        return 'Не подписан на курс'

    class Meta:
        model = Course
        fields = ('__all__')


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ('__all__')
