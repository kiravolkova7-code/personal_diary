from django.db import models
from users.models import User


class Entry(models.Model):
    """Модель записи в дневнике"""

    SUBJECT_CHOICES = (
        ('work', 'Работа'),
        ('personal', 'Личное'),
        ('travels', 'Путешествия'),
        ('other', 'Другое')
    )

    title = models.CharField('Заголовок', max_length=255)
    subject = models.CharField(
        verbose_name='Тема / Категория',
        choices=SUBJECT_CHOICES,
        default='other',
        max_length=20
    )
    content = models.TextField('Текст записи')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f'{self.title[:30]}... от {self.user.email}'


