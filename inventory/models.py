from django.db import models

class Job(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    units = models.CharField(max_length=20)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __unicode__(self):
        return self.name

class Order(models.Model):
    employee = models.ForeignKey(Employee)
    job = models.ForeignKey(Job)
    message = models.TextField()

class LineItem(models.Model):
    order = models.ForeignKey(Order)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField()

    def __unicode__(self):
        return str(self.item) + ":" + self.quantity

