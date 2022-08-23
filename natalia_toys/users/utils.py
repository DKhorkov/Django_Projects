from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


def send_email_for_verify(request, user):
    """Функция для отправки письма-подтверждения на почту для верификации пользователя."""

    # Основа взята с базовой формы сброса пароля.
    current_site = get_current_site(request)  # Получение домена сайта.
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }

    # Передача шаблона в контекст, рендеринг и возврат шаблона в виде строки:
    message = render_to_string(
        'registration/verify_email.html',
        context=context,
    )

    email = EmailMessage(
        'Подтверждение адреса электронной почты',  # Заголовок.
        message,  # Тело сообщения.
        to=[user.email],  # Адресат.
    )
    email.send()
