from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='profiles', max_length=254, blank=True)
    phone = models.CharField(max_length=60)
    is_mechanic = models.BooleanField(default=False)
    customer_id = models.CharField(max_length=160)

class Mechanic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lat = models.DecimalField(max_digits=10,decimal_places=4)
    lon = models.DecimalField(max_digits=10,decimal_places=4)
    address = models.CharField(max_length=120)
    garage = models.CharField(max_length=120)
    is_searching = models.BooleanField(default=True)
    insurance = models.CharField(max_length=120)
    license = models.CharField(max_length=120)
    is_verified = models.BooleanField(default=False)
    license_image = models.ImageField(upload_to='documents',max_length=254, blank=True)
    def __str__(self):
        return self.user.email

class Codes(models.Model):
   code = models.CharField('code',max_length = 60)
   mechanic= models.ForeignKey(Mechanic, on_delete=models.CASCADE)
   def __str__(self):
        return self.code

class Manufacturer(models.Model):
    company = models.CharField(max_length=160)
    def __str__(self):
        return self.company

class Car(models.Model):
    manufacturer= models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    year= models.CharField(max_length=120)
    trim= models.CharField(max_length=120)
    medium_fee = models.DecimalField(max_digits=10,decimal_places=2)
    grade_fee = models.DecimalField(max_digits=10,decimal_places=2)
    conventional_fee = models.DecimalField(max_digits=10,decimal_places=2)
    premium_fee = models.DecimalField(max_digits=10,decimal_places=2)
    image= models.ImageField(upload_to='vehicles',max_length=160)
    user= models.ManyToManyField(User, null=True, blank=True)
    def __str__(self):
        return self.manufacturer.company

class Notifications(models.Model):
   title = models.CharField(max_length = 60)
   body = models.CharField(max_length = 60)
   data = models.CharField(max_length = 60)
   image= models.CharField(max_length=160)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   user= models.ForeignKey(User, on_delete=models.CASCADE)
   def __str__(self):
        return self.title

class Appointment(models.Model):
    date= models.DateTimeField()
    fee= models.DecimalField(max_digits=10,decimal_places=2)
    zip_code= models.CharField(max_length=60)
    service= models.CharField(max_length=120)
    address= models.CharField(max_length=300)
    lat = models.DecimalField(max_digits=10,decimal_places=6)
    lon = models.DecimalField(max_digits=10,decimal_places=6)
    is_payed = models.BooleanField(default=False)
    grade= models.CharField(max_length=120, null=True, blank=True)
    instructions= models.CharField(max_length=240, null=True, blank=True)
    status= models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    car= models.ForeignKey(Car, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.service
