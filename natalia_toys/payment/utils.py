from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def send_cheque(request, user, order):
    """Функция для отправки чека о покупке пользователем игрушки/игрушек."""
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'order': order,
    }

    # Передача шаблона в контекст, рендеринг и возврат шаблона в виде строки:
    message = render_to_string(
        'payment/send_cheque.html',
        context=context,
    )

    email = EmailMessage(
        f'Чек об оплате заказа №{order.id}',  # Заголовок.
        message,  # Тело сообщения.
        to=[user.email, order.email],  # Адресат.
    )
    email.send()


def send_notification(request, user, order, payment_id):
    """Функция для отправки уведомления владельцу о покупке пользователем игрушки/игрушек."""
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'order': order,
        'payment_id': payment_id
    }

    # Передача шаблона в контекст, рендеринг и возврат шаблона в виде строки:
    message = render_to_string(
        'payment/send_notification.html',
        context=context,
    )

    email = EmailMessage(
        f'Заказ №{order.id} был оплачен',  # Заголовок.
        message,  # Тело сообщения.
        to=[settings.EMAIL_HOST_USER],  # Адресат.
    )
    email.send()
