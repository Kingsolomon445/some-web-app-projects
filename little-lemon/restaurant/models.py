from django.db import models


# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self):
        return self.first_name


# Add code to create Menu model
class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(null=False)
    description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return f'{self.name} : {self.description}'

    def calculate_total_cost(self):
        # calculate the total cost of all the items on the menu
        total_cost = self.price + 10
        return total_cost
