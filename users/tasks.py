from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True)
def send_welcome_email(self, user_email, username):
    try:
        subject = "Добро пожаловать в личный дневник!"
        message = f"Привет, {username}! Рады видеть вас."
        send_mail(subject, message, "noreply@yourdiary.ru", [user_email])
    except Exception as e:
        # Если упала ошибка сети, просим Celery повторить попытку через 10 секунд
        raise self.retry(exc=e, countdown=10)
