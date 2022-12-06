from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from authapp.models import User


@shared_task  # Именно этот декоратор делает функцию - таской celery
def send_feedback_to_email(message_from: str, message_body: str) -> None:
    '''
    Функция для отправки сообщений клиентов с формы на сайте
    :param message_from: от кого
    :param message_body: тело обращения
    :return:
    '''
    user_from = User.objects.filter(email=message_from).first().get_full_name()
    send_mail(
        subject=f'Feedback from: {user_from}, {message_from}',  # Тема
        message=message_body,  # Тело обращения
        recipient_list=['pospeev.artem@icloud.com', ],  # Список получателей
        from_email=settings.EMAIL_HOST_USER,  # От кого
        fail_silently=False,  # Уведомлять об ошибках. По умолчанию True - не уведомлять
    )
