import random

from templated_mail.mail import BaseEmailMessage

from auth_system.services.cache_function import setKey


class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activation_code'] = random.randint(100000, 999999)

        setKey(
            key=context.get('user').email,
            value=context.get('activation_code'),
            timeout=None
        )
        return context
