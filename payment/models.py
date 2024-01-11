from django.db import models
from study.models import Course, Lesson, NULLABLE
from users.models import User


class Payment(models.Model):
    PAY_CARD = 'card'
    PAY_CASH = 'cash'

    PAY_TYPES = (
        (PAY_CASH, 'Наличные'),
        (PAY_CARD, 'Перевод на счет')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    date_of_payment = models.DateField(verbose_name='Дата оплаты', **NULLABLE, auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    amount_payment = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    method_payment = models.CharField(max_length=20, choices=PAY_TYPES, verbose_name='Способ оплаты')
    stripe_id = models.CharField(max_length=300, verbose_name='stripe_id', **NULLABLE)

    def __str__(self):
        return f'{self.paid_course if self.paid_course else self.paid_lesson} - {self.amount_payment}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
