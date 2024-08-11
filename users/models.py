from django.db import models
from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="email", unique=True)
    avatar = models.ImageField(
        upload_to="media/users/",
        verbose_name="Аватар",
        help_text="Укажите аватар",
        **NULLABLE
    )
    telephone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        help_text="Введите телефон",
        **NULLABLE
    )
    city = models.CharField(
        max_length=35,
        verbose_name="город",
        help_text="Введите город",
        **NULLABLE
    )
    token = models.CharField(
        max_length=50,
        verbose_name="токен",
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"


class Payment(models.Model):
    PAYMENT_CASH = 'cash'
    PAYMENT_TRANSFER = 'transfer'
    PAYMENT_CHOICES = (
        (PAYMENT_CASH, 'Оплата наличными'),
        (PAYMENT_TRANSFER, 'Перевод на счет'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    date_payment = models.DateTimeField(verbose_name='дата оплаты', auto_now_add=True)
    lesson_paid = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    course_paid = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='сумма оплаты', **NULLABLE)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES, verbose_name='тип оплаты', **NULLABLE)
    payment_link = models.URLField(max_length=400, verbose_name='ссылка для оплаты', **NULLABLE)

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'

    def __str__(self):
        return f'{self.user.email} - {self.lesson_paid.title if self.lesson_paid else self.course_paid.title}'
