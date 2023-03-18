from django.db import models

# Create your models here.
class Truck(models.Model):
    Truck_id = models.AutoField(primary_key=True)
    Truck_brand = models.CharField(max_length=100)
    Truck_model= models.CharField(max_length=100, null=True, blank=True)
    Plate_number = models.CharField(max_length=20, unique=True,null=True,blank=True)
    Registration_number = models.CharField(max_length=20, unique=True,null=True,blank=True)
    def __str__(self):
         return f'{self.Plate_number}'
     
class Driver(models.Model):
    Driver_id = models.AutoField(primary_key=True)
    Driver_name = models.CharField(max_length=100)
    Mobile_number = models.CharField(max_length=100, null=True, blank=True,unique=True,)
    Email = models.EmailField(max_length=100,unique=True, null=True, blank=True)
    City = models.CharField(max_length=100, null=True, blank=True)
    District = models.CharField(max_length=100, null=True, blank=True)
    Language = models.CharField(max_length=100, null=True, blank=True)
    Truck = models.ForeignKey(Truck, on_delete=models.DO_NOTHING, null=True, blank=True)
    def __str__(self):
         return f'{self.Driver_name}, {self.Email}'