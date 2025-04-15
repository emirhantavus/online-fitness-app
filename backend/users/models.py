from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin , Group ,Permission
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserManager(BaseUserManager):
      def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError('The Email field must be set')
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

      def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)

            if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('Superuser must have is_superuser=True.')

            return self.create_user(email, password, **extra_fields)
  
class User(AbstractBaseUser, PermissionsMixin):
      email = models.EmailField(unique=True)
      first_name = models.CharField(max_length=30, blank=True)
      last_name = models.CharField(max_length=30, blank=True)
      is_staff = models.BooleanField(default=False)
      is_active = models.BooleanField(default=True)
      date_joined = models.DateTimeField(auto_now_add=True)
      is_trainer = models.BooleanField(default=False)
      monthly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Eğitmenler için aylık ücret
      
      groups = models.ManyToManyField(
          Group,
          related_name='custom_user_groups',
          blank=True,
      )
      user_permissions = models.ManyToManyField(
          Permission,
          related_name='custom_user_permissions',
          blank=True,
      )     
      objects = CustomUserManager() 
      USERNAME_FIELD = 'email'
      REQUIRED_FIELDS = []    
      
      def __str__(self):
            return self.email     
      @property
      def is_student(self):
          return not self.is_trainer      
      def tokens(self):
          refresh = RefreshToken.for_user(self)
          return {
              'refresh': str(refresh),
              'access': str(refresh.access_token),
          }
          
      def get_full_name(self):
            return f"{self.first_name} {self.last_name}".strip()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.email