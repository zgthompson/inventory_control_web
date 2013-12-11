from django.db import models
from datetime import datetime

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
    employee = models.ForeignKey(Employee, null=True, blank=True)
    job = models.ForeignKey(Job, null=True, blank=True)
    message = models.TextField(blank=True, default="")
    employee_name = models.CharField(max_length=100, blank=True, default="")
    job_name = models.CharField(max_length=100, blank=True, default="")
    date_ordered = models.DateTimeField('date ordered', default=datetime.now)
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return "Order " + str(self.id)

    def save(self, *args, **kwargs):
        if self.employee and self.job:
            self.completed = True
        else:
            self.completed = False 
        models.Model.save(self, *args, **kwargs)

#    def pending(self):
#        return not self.employee or not self.job

    def show_employee(self):
        if self.employee:
            return str(self.employee)
        elif self.employee_name:
            return self.employee_name
        else:
            return None

    def show_job(self):
        if self.job:
            return str(self.job)
        elif self.job_name:
            return self.job_name
        else:
            return None

class LineItem(models.Model):
    order = models.ForeignKey(Order)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField()

    def __unicode__(self):
        return str(self.item) + ":" + str(self.quantity)

