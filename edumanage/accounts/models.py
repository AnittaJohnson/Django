from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, school_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            school_name=school_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, school_name, password=None):
        user = self.create_user(
            email=email,
            school_name=school_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    ORGANIZATION_CHOICES = [
        ('school', 'School'),
        ('college', 'College'),
    ]
    
    COUNTRY_CHOICES = [
        ('us', 'United States'),
        ('uk', 'United Kingdom'),
        ('in', 'India'),
        # Add more countries as needed
    ]
    
    school_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address_area = models.CharField(max_length=100)
    address_landmark = models.CharField(max_length=100, blank=True, null=True)
    address_city = models.CharField(max_length=50)
    address_state = models.CharField(max_length=50)
    address_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES)
    address_pincode = models.CharField(max_length=10)
    organization_type = models.CharField(max_length=10, choices=ORGANIZATION_CHOICES)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['school_name']
    
    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin

class SchoolRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.school_name


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15)
    fathers_name = models.CharField(max_length=100)
    dob = models.DateField()
    roll_no = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    school = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate with school

    def __str__(self):
        return self.name