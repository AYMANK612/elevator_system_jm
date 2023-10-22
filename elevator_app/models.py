from django.db import models

# Create your models here.
class Elevator(models.Model):
    name=models.CharField(max_length=25)
    current_floor = models.IntegerField(default=1)
    is_working = models.BooleanField(default=True)
    is_door_open = models.BooleanField(default=False)
    is_moving_up=models.BooleanField(default=False)

class Request(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)