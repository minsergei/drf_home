from django.db import models
from config import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="media/materials/course",
        verbose_name="картинка",
        help_text="Добавьте превью изображения",
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="описание курса", help_text="Укажите описание курса"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="название урока", help_text="Укажите название урок"
    )
    description = models.TextField(
        verbose_name="описание урока", help_text="Укажите описание урока"
    )
    preview = models.ImageField(
        upload_to="media/materials/lesson",
        verbose_name="картинка",
        help_text="Добавьте превью изображения",
        **NULLABLE,
    )
    link = models.URLField(
        max_length=200,
        verbose_name="ссылка на видео",
        help_text="Укажите ссылку на видео",
        **NULLABLE,
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.SET_NULL,
        verbose_name="Название курса",
        help_text="Выберите курс",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
