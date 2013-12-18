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
        if  not self.completed and self.employee and self.job:
            self.completed = True
            for line_item in self.lineitem_set.all():
                line_item.add_or_update_stockchange()

        if self.employee:
            self.employee_name = self.employee.name

        if self.job:
            self.job_name = self.job.name

        models.Model.save(self, *args, **kwargs)

class LineItem(models.Model):
    order = models.ForeignKey(Order)
    item = models.ForeignKey(Item)
    quantity = models.IntegerField()

    def __unicode__(self):
        return str(self.item) + ":" + str(self.quantity)

    def add_or_update_stockchange(self):
        if self.has_stockchange():
            self.stockchange.item = self.item
            self.stockchange.quantity = self.quantity
            self.stockchange.save()
        else:
            StockChange.objects.create(item=self.item, quantity=self.quantity, direction='OUT', line_item=self)


    def has_stockchange(self):
        try:
            self.stockchange
            return True
        except:
            return False

    def save(self, *args, **kwargs):
        models.Model.save(self, *args, **kwargs)

        if self.order.completed:
            self.add_or_update_stockchange()

class StockChange(models.Model):
    IN_OR_OUT = ( ('IN', 'IN'), ('OUT', 'OUT') )

    item = models.ForeignKey(Item)
    quantity = models.IntegerField()
    direction = models.CharField(max_length=3, choices=IN_OR_OUT)
    date_changed = models.DateTimeField('date changed', auto_now=True, default=None)
    line_item = models.OneToOneField(LineItem, blank=True, null=True)

    def __unicode__(self):
        return "Stock Change " + str(self.id)

