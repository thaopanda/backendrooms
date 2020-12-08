from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

USER_TYPE = [(_, _) for _ in ('Host', 'Renter')]

class UserManager(BaseUserManager):
 
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
 

class RenterAndAdminManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class HostManager(BaseUserManager):
    def create_user(self, email, username, fullname, identication, address, phoneNumber, password=None):
        if not email:
            raise ValueError('Host must have an email address')
        if not username:
            raise ValueError('Host must have a username')
        if not fullname:
            raise ValueError('Host must have fullname')
        if not identication:
            raise ValueError('Host must have identication')
        if not address:
            raise ValueError('Host mus have address')
        if not phoneNumber:
            raise ValueError('Host must have phoneNumber')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            fullname = fullname,
            identication = identication,
            address = address,
            phoneNumber = phoneNumber,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    # user_type = models.CharField(choices=USER_TYPE, null=False, blank=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

class Host(MyUser):
    fullname = models.CharField(max_length=50, unique=False)
    identication = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=20, unique=True)
    is_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname', 'identication', 'address', 'phoneNumber']

    objects = HostManager()

    def __str__(self):
        return self.username


class Renter(MyUser):
    fullname = models.CharField(max_length=50, unique=False, blank=True, null=True)
    interested_area = models.CharField(max_length=200, unique=False, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username

    objects = RenterAndAdminManager()


