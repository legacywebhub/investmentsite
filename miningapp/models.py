from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

# Manager class for custom user
class UserManager(BaseUserManager):
    # Determines how to create our user model and validations
    def create_user(self, email, password=None):
        # Use this check for as many field you want
        if not email:
            raise ValueError("email is required")


        user = self.model(
            # normalize_email ensures our email is properly formatted
            email = self.normalize_email(email),
        )
        # Setting password for user
        user.set_password(password)
        # Saving user to database
        user.save(using=self._db)
        # Return user after saving
        return user

    # Determines how to create superuser
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password
        )
        # Granting permissions to the super user
        user.is_staff = True
        user.is_superuser = True
        # Saving user to database
        user.save(using=self._db)
        # Return user after saving
        return user

    '''
    Make sure to set this manager as the manager in your custom model
    objects = MyUserManager()
    '''





# Custom user model class
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(verbose_name="first name", max_length=60)
    last_name = models.CharField(verbose_name="last name", max_length=60)
    username = models.CharField(verbose_name="username", max_length=30, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name="email address", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    # Setting to determing what field to use as login parameter
    USERNAME_FIELD = "email"

    # Setting to set required fields
    REQUIRED_FIELDS = []

    # Setting a manager for this custom user model
    objects = UserManager()

    # Setting to determine what field to show on our database
    def __str__(self):
        return self.name

    # Determines if signup user has permissions
    def has_perm(self, perm, obj=None):
        return True

    # Determines if the signed up user will have acccess to other models
    # In our app or project
    def has_module_perms(self, app_label):
        return True

    # Function to get url per user for sitemapping
    def get_absolute_url(self):
        return f'/profile/{self.id}'

    '''
    Make sure to set this custom model as our user model in settings.py
    AUTH_USER_MODEL = "App.CustomUserModel"
    Make sure to delete previous migration files incase of errors
    Then make migrations
    '''



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    profile_pic = models.ImageField(upload_to="images/profiles", null=True, blank=True)
    wallet_address = models.CharField(max_length=60, null=True, blank=True)
    ref_code = models.CharField(verbose_name="referral code", max_length=30, unique=True, null=True, blank=True)
    upline = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="upline", related_name="upline")
    downlines = models.ManyToManyField(User, verbose_name="referred", related_name="downline")

    def __str__(self):
        return self.user.username


class CompanyInfo(models.Model):
    logo = models.ImageField(upload_to="images/company", blank=True, null=True)
    name = models.CharField(max_length=150, blank=False, null=False)
    address = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=60, blank=True, null=True)
    email1 = models.EmailField(blank=False, null=False)
    email2 = models.EmailField(blank=True, null=True)
    phone1 = models.CharField(max_length=25, blank=False, null=False)
    phone2 = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id and CompanyInfo.objects.exists():
            raise ValueError("This model cannot have two or more records")
        else:
            super().save(*args, **kwargs)



class Message(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=3000, null=False, blank=False)
    date_received = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.date_received}'
