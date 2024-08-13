from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscribe
from materials.paginators import ResultsSetPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from django_filters.rest_framework import DjangoFilterBackend

from users.permissions import IsModerator, IsOwner
from materials.tasks import send_email


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = ResultsSetPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        update_course = serializer.save()
        send_email.delay(update_course.id)
        update_course.save()

    def get_permissions(self):
        '''Назначаем права на действия с объектами'''
        if self.action == 'create':
            self.permission_classes = (~IsModerator, IsAuthenticated,)
        elif self.action in ['update', 'retrieve', 'partial_update']:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner | ~IsModerator,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = ResultsSetPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner,)


class SubscribeCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def post(self, *args, **kwargs):

        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item, created = Subscribe.objects.get_or_create(user=user, course=course_item)

        if created:
            message = 'Вы подписались на обновления курса'
            status_code = status.HTTP_201_CREATED
        else:
            subs_item.delete()
            message = 'Вы отписались от обновления курса'
            status_code = status.HTTP_204_NO_CONTENT
        return Response({"message": message}, status=status_code)


class SubscribeListAPIView(generics.ListAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
