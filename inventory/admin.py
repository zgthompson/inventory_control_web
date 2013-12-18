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
    search_fields = ['job__name', 'job__number',  'employee__name']
    list_filter = ['date_ordered', 'completed']
    list_display = ['__unicode__', 'job_name', 'employee_name', 'date_ordered', 'completed']
    fields = [('job', 'job_name'), ('employee', 'employee_name'), 'date_ordered', 'message']
    raw_id_fields = ['job', 'employee']
    inlines = [LineItemInline]

    def get_form(self, request, obj=None, **kwargs):
        self.fields = ['job', 'employee', 'date_ordered', 'message']
        if obj:
            if not obj.job:
                self.fields[0] = ('job', 'job_name')
            if not obj.employee:
                self.fields[1] = ('employee', 'employee_name')
        return super(OrderAdmin, self).get_form(request, obj=None, **kwargs)

class StockChangeAdmin(admin.ModelAdmin):
    search_fields = ['item__name', 'line_item__order__job_name', 'line_item__order__job__number', 'line_item__order__employee_name']
    list_filter = ['date_changed', 'direction']
    exclude = ['line_item']
    raw_id_fields = ['item']
    list_display = ['item', 'quantity', 'direction', 'date_changed']

    def __init__(self, *args, **kwargs):
        super(StockChangeAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ( None, )

    def has_delete_permission(self, request, obj=None):
        print obj
        print not obj
        return not obj


admin.site.register(Job, JobAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(StockChange, StockChangeAdmin)
