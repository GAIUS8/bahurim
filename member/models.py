from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=MyUserManager.normalize_email(email),
            name=name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        u = self.create_user(email=email,
                             name=name,
                             password=password,
                             )
        u.is_admin = True
        u.save(using=self._db)
        return u


class MyUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICE = (
        ('MALE', '남자'),
        ('FEMALE', '여자'),
        ('OTHER', '기타'),
    )
    
    email = models.EmailField(unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='실명')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default='OTHER',)
    birthday = models.DateField(blank=True, null=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']