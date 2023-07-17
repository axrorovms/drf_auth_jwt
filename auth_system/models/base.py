__all__ = ('BaseAbstractUser',)

from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import CharField, EmailField, BooleanField, DateTimeField, DecimalField, ImageField

from auth_system.models.manager import BaseManagerUser
from auth_system.services.upload_files import upload_name


class BaseAbstractUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    first_name = CharField(_("first name"), max_length=150, blank=True)
    last_name = CharField(_("last name"), max_length=150, blank=True)
    phone = CharField(_("phone"), max_length=50, blank=True)
    balance = DecimalField(_("balance"), max_digits=1000, decimal_places=2, default=0)
    image = ImageField(upload_to=upload_name, blank=True)

    email = EmailField(_("email"),
                       unique=True,
                       help_text=_("Required. exsample@mail.com"),
                       validators=[email_validator],
                       error_messages={"unique": _("A user with that email already exists.")},
                       )

    username = CharField(_("username"),
                         max_length=150,
                         unique=True,
                         help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
                         validators=[username_validator],
                         error_messages={"unique": _("A user with that username already exists.")},
                         )

    subscription = BooleanField(_('subscription'), default=False)

    is_staff = BooleanField(_("staff status"),
                            default=False,
                            help_text=_("Designates whether the user can log into this admin site."))

    is_active = BooleanField(_("active"),
                             default=False,
                             help_text=_(
                                 "Designates whether this user should be treated as active. "
                                 "Unselect this instead of deleting accounts."))

    is_moderator = BooleanField(_("moderator"),
                                default=False,
                                help_text=_(
                                    "This specifies whether the user should be considered a moderator."
                                    "Unselect this instead of deleting accounts."))
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    objects = BaseManagerUser()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['id', 'email']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
