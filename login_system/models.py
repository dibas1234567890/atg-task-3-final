from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

choices_status = [
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    ]

class CustomUserManager(AbstractUserManager):
    def get_all_patients(self):
        return self.get_queryset().filter(user_type = 'patient')
    def get_all_doctors(self):
        return self.get_queryset().filter(user_type = 'doctor')
    def get_by_user_type(self, user_type):
        return self.get_queryset().get(user_type = user_type)

class CustomerUserProfile(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100) 
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(  max_length=10)
    user_type = models.CharField( choices= [('patient', 'patient'),( 'doctor','doctor')] , max_length=10)
    calendar_id = models.CharField(max_length=255, blank=True, null=True)
    custommanager = CustomUserManager()

class Category(models.Model):

   
    category_name = models.CharField(max_length=50)
    category_slug = models.SlugField()

class BlogModel(models.Model): 
     
    title = models.CharField( max_length=256)
    image = models.ImageField()
    category =  models.CharField( max_length=256)
    summary =  models.CharField( max_length=256)
    content = models.CharField( max_length=256)
    status = models.CharField( choices=choices_status, max_length=128)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerUserProfile, on_delete=models.CASCADE,)

        
from django.db import models

class Event(models.Model):
    summary = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Appointment(models.Model):
    doctor = models.ForeignKey(CustomerUserProfile, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    date = models.CharField(max_length=256)
    start_time = models.CharField(max_length=256)
    end_time = models.CharField(max_length=256, null=True, blank=True)
    patient = models.ForeignKey(CustomerUserProfile, blank=True, null=True, 
                                on_delete=models.CASCADE, related_name='patient_appointment')


    

    def __str__(self):
        return f"Appointment with Dr. {self.doctor} on {self.date} at {self.start_time}"
class CalendarModel(models.Model):
    doctor = models.OneToOneField(CustomerUserProfile, on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=255, unique=True)
    summary = models.CharField(max_length=255)
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    patient = models.ForeignKey(CustomerUserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='patient')

    

