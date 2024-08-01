from django.contrib import admin

from users.models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email",)



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_payment', 'lesson_paid', 'course_paid', 'amount')
