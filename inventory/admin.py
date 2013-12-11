from django.contrib import admin

from inventory.models import *

class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 1

class JobAdmin(admin.ModelAdmin):
    search_fields = ['number', 'name']
    list_display = ['number', 'name']

class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'price', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['job__name', 'employee__name']
    list_filter = ['date_ordered', 'completed']
    list_display = ['__unicode__', 'show_job', 'show_employee', 'date_ordered', 'completed']
    fields = [('job', 'job_name'), ('employee', 'employee_name'), 'date_ordered', 'message']
    inlines = [LineItemInline]

admin.site.register(Job, JobAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
