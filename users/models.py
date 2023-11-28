from django.db import models 
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import ( AbstractBaseUser , PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from App.utils.models import (PersonBaseModel, AppModel)
from django.conf import settings


class Users(AbstractBaseUser ,  PermissionsMixin ,  PersonBaseModel ):
    email        = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username     = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(blank=True , default=None , null=True , upload_to='storage/users/avatar')
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now())
    language = models.CharField(max_length=10,choices=settings.LANGUAGES,default=settings.LANGUAGE_CODE)
    verified_on = models.DateTimeField(_('emailed verification date') , null=True)

    # The following fields are required for every customer User model
    last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
    date_joined  = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()
    
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
        
    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return self.first_name+" "+self.last_name
    
    
    class Meta:
        db_table = 'users'
        verbose_name = _("user")
        verbose_name_plural = _("users")
        
class UserSettings(AppModel):
    user = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
    class Meta:
        db_table = 'users_settings'
        verbose_name = _("user setting")
        verbose_name_plural = _("users settings")
        

class ValidationCodes (AppModel):
    CODE_FOR = [
        ('PWR' , _('Password Reset code')),
        ('PNV' , _('Phone NUmber Validation')),
        ('UVC' , _('User verification Code')),
    ]
    
    user = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
    reset_code = models.TextField(verbose_name=_('reset code') , max_length=6 , null=False , blank=False)
    code_for = models.CharField(max_length=3 , choices=CODE_FOR)
    
    class Meta:
        db_table = 'validation_codes'
        verbose_name = _("Validation Code")
        verbose_name_plural = _("Validation Codes")