from django.db import models
from django.urls import reverse
from django.contrib import admin 
from django.contrib.auth.models import User
import datetime

# Shuttle Model
class Shuttle(models.Model):
    shuttle_name = models.CharField(max_length=200)
    shuttle_capacity = models.IntegerField()
    class Meta:
        verbose_name = "Shuttle Detail"
        verbose_name_plural = "Shuttle Details"
    def get_absolute_url(self):
        """Returns the url to access a particular shuttle instance."""
        return reverse('shuttle-detail', args=[str(self.id)])

    def __str__(self):
        return self.shuttle_name
    
class GreenShuttle(models.Model):
    mu_name = models.CharField(max_length=200, default='Green') 
    stop_name = models.CharField(max_length=200)
    number_of_passangers_in = models.PositiveIntegerField(default=0)
    number_of_passangers_out = models.PositiveIntegerField(default=0)
    date = models.DateField(null=True , blank=True , auto_now_add=True)  
    time = models.TimeField(null=True , blank=True, auto_now_add=True)
    shuttle_driver = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,)
    shuttle_detail = models.ForeignKey(Shuttle, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Green Shuttle Entry"
        verbose_name_plural = "Green Shuttle Entries"

    def get_absolute_url(self):
        """Returns the url to access a particular location instance."""
        return reverse('green-detail', args=[str(self.id)])
    def __str__(self):
        return f"{self.mu_name}"
    
class greenShuttleStopIndex(models.Model):
    green_index_value = models.IntegerField(default=0)
    class Meta:
        verbose_name = "Green Shuttle Stop Index"
        verbose_name_plural = "Green Shuttle Stop Index "
    def __str__(self):
        return f"Current Index: {self.green_index_value}"
    
class LastStopGreenOccupancy(models.Model):
    green_occupancy = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Green Last Stop Occupancy"
        verbose_name_plural = "Green Last Stop Occupancy"
    def __str__(self):
        return f"Current Occupancy: {self.green_occupancy}"
    
    
    
class BlueShuttle(models.Model):
    mu_name = models.CharField(max_length=200, default='Blue') 
    stop_name = models.CharField(max_length=200)
    number_of_passangers_in = models.PositiveIntegerField(default=0)
    number_of_passangers_out = models.PositiveIntegerField( default=0)
    date = models.DateField(null=True , blank=True,auto_now_add=True)  
    time = models.TimeField(null=True ,blank=True, auto_now_add=True)
    occupancy_detail = models.IntegerField(default=0)
    shuttle_driver = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,)
    shuttle_detail = models.ForeignKey(Shuttle, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Blue Shuttle Entry"
        verbose_name_plural = "Blue Shuttle Entries"
    def get_absolute_url(self):
        """Returns the url to access a particular location instance."""
        return reverse('blue-detail', args=[str(self.id)])
    def __str__(self):
        return f"{self.mu_name}"

class ShuttleStopIndex(models.Model):
    blue_index_value = models.IntegerField(default=0)
    class Meta:
        verbose_name = "Blue Shuttle Stop Index"
        verbose_name_plural = "Blue Shuttle Stop Index"
    def __str__(self):
        return f"Current Index: {self.blue_index_value}"
    
class LastStopBlueOccupancy(models.Model):
    blue_occupancy = models.IntegerField(default=0)
    class Meta:
        verbose_name = "Blue Last Stop Occupancy"
        verbose_name_plural = "Blue Last Stop Occupancy"
    def __str__(self):
        return f"Current Occupancy: {self.blue_occupancy}"

