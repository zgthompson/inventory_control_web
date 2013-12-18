from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db.models import Q
from django.core.mail import EmailMessage
import operator
import json
from inventory.models import *

@dajaxice_register
def search_jobs(request, query):
    dajax = Dajax()
    q_list = []
    for word in query.strip().split(" "):
        q_list.append( Q( name__icontains = word) )

    jobs = Job.objects.filter( reduce(operator.and_, q_list) | Q( number__icontains = query) )[:5]

    if jobs:
        out = ["<table class='table table-striped table-bordered table-hover'><tr><th>Number</th><th>Name</th><th></th></tr>"]
        for job in jobs:
            out.append("<tr><td>%s</td><td>%s</td><td><button class='btn' data='%s' onclick='orderFormAdmin.select_job(this);'>Select</button></td></tr>" % (job.number, job.name,  job.id) )
        out.append("</table>")
    else:
        out = ["No jobs found"]
    dajax.assign('#job-results', 'innerHTML', ''.join(out))

    return dajax.json()

@dajaxice_register
def search_employees(request, query):
    dajax = Dajax()
    q_list = []
    for word in query.strip().split(" "):
        q_list.append( Q( name__icontains = word) )

    employees = Employee.objects.filter( reduce(operator.and_, q_list) )[:5]

    if employees:
        out = ["<table class='table table-striped table-bordered table-hover'><tr><th>Name</th><th></th></tr>"]
        for employee in employees:
            out.append("<tr><td>%s</td><td><button class='btn' data='%s' onclick='orderFormAdmin.select_employee(this);'>Select</button></td></tr>" % (employee.name, employee.id) )
        out.append("</table>")
    else:
        out = ["No employees found"]
    dajax.assign('#employee-results', 'innerHTML', ''.join(out))

    return dajax.json()





@dajaxice_register
def search_items(request, query):
    dajax = Dajax()

    q_list = []
    for word in query.strip().split(" "):
        q_list.append( Q( name__icontains = word) )

    items = Item.objects.filter( reduce(operator.and_, q_list) )[:10]

    if items:
        out = ["<table class='table table-striped table-bordered table-hover'><tr><th>Item</th><th>Amount</th><th>Units</th><th></th></tr>"]
        for item in items:
            out.append("<tr><td>%s</td><td><input type='text' name='quantity' autocomplete='off' placeholder='0'></td><td>%s</td><td><button class='btn' data='%s' onclick='orderForm.add_item(this);'>Add</button></td></tr>" % (item.name, item.units, item.id) )
        out.append("</table>")
    else:
        out = ["No items found"]
    dajax.assign('#item-results', 'innerHTML', ''.join(out))

    return dajax.json()

@dajaxice_register
def add_order(request, order_json):
    order_data = json.loads(order_json)

    order = Order.objects.create()

    for key, value in order_data['line_items'].items():
        LineItem.objects.create(item_id=key, quantity=value['quantity'], order_id = order.id)

    if 'employee' in order_data:
        order.employee = Employee.objects.get(id=order_data['employee'])
    else:
        order.employee_name = order_data['employee_name']

    if 'job' in order_data:
        order.job = Job.objects.get(id=order_data['job'])
    else:
        order.job_name = order_data['job_name']

    if 'message' in order_data:
        order.message = order_data['message']

    order.save()

    if not order.completed:
        email = EmailMessage('New order', order_to_email(order), to=['zgthompson@gmail.com'])
        email.send()

def email_line(header, data):
    return str(header).title() + ": " + str(data) + "\n"

def order_to_email(order):
    out = email_line("date", order.date_ordered.strftime("%A, %B %d, %Y %I:%M%p")) + "\n\n"
    out += email_line("job", order.job_name)
    out += email_line("employee", order.employee_name)
    line_items = order.lineitem_set.all()

    if line_items:
        out += "\nItems\n"
        for line_item in line_items:
            out += email_line(line_item.item.name, str(line_item.quantity) + " " + line_item.item.units)

    if order.message:
        out += "\nMessage\n" + order.message + "\n\n"

    out += "View order: localhost:8000/admin/inventory/order/" + str(order.id)
    return out

