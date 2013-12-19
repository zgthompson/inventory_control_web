from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
import operator
import json
from datetime import date
from datetime import time
from inventory.models import *

@dajaxice_register
def items_out(request, begin, end):
    return item_report(request, begin, end, "OUT")

@dajaxice_register
def items_in(request, begin, end):
    return item_report(request, begin, end, "IN")

def item_report(request, begin, end, direction):
    dajax = Dajax()

    start_date = string_to_date(begin)
    end_date = string_to_date(end)
    end_date = datetime.combine(end_date, time(23, 59, 59, 999999))

    stock_changes = StockChange.objects.filter( date_changed__range=(start_date, end_date), direction=direction )

    totals = {}

    for stock_change in stock_changes:
        if stock_change.item.id in totals:
            totals[stock_change.item.id]['amount'] += stock_change.quantity
        else:
            totals[stock_change.item.id] = {}
            totals[stock_change.item.id]['amount'] = stock_change.quantity
            totals[stock_change.item.id]['unit_cost'] = stock_change.item.price
            totals[stock_change.item.id]['units'] = stock_change.item.units
            totals[stock_change.item.id]['name'] = stock_change.item.name

    if totals:
        out = ["<table id='report-table' class='table table-condensed tablesorter'><thead><tr><th>Item</th><th>Amount</th><th>Total Cost</th></tr></thead><tbody>"]
        for item in totals.itervalues():
            out.append("<tr><td>%s</td><td>%s %s</td><td>$%s</td></tr>" % ( item['name'], item['amount'], item['units'], item['amount'] * item['unit_cost'] ))
        out.append("</tbody></table>")
    else:
        out = ["No results for this date range"]

    dajax.assign('#report-results', 'innerHTML', ''.join(out))

    if totals:
        dajax.script('report.attach_tablesorter();')

    return dajax.json()

@dajaxice_register
def job_cost(request, begin, end):
    dajax = Dajax()

    start_date = string_to_date(begin)
    end_date = string_to_date(end)
    end_date = datetime.combine(end_date, time(23, 59, 59, 999999))

    orders = Order.objects.filter( date_ordered__range=(start_date, end_date), completed=True )

    totals = {}

    for order in orders:
        cur_total = 0
        for line_item in order.lineitem_set.all():
            cur_total += line_item.item.price * line_item.quantity
        if order.job.id in totals:
            totals[order.job.id]['total'] += cur_total
        else:
            totals[order.job.id] = {}
            totals[order.job.id]['name'] = order.job.name
            totals[order.job.id]['number'] = order.job.number
            totals[order.job.id]['total'] = cur_total

    if totals:
        out = ["<table id='report-table' class='table table-condensed tablesorter'><thead><tr><th>Job number</th><th>Job name</th><th>Total</th></tr></thead><tbody>"]
        for job in totals.itervalues():
            out.append("<tr><td>%s</td><td>%s</td><td>$%s</td></tr>" % ( job['number'], job['name'], job['total'] ) )
        out.append("</tbody></table>")
    else:
        out = ["No results for this date range"]
    dajax.assign('#report-results', 'innerHTML', ''.join(out))

    if totals:
        dajax.script('report.attach_tablesorter();')

    return dajax.json()

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
        email = EmailMultiAlternatives('New order', order_to_plaintext(order), to=['zgthompson@gmail.com'])
        email.attach_alternative(order_to_html(order), "text/html")
        email.send()



def order_to_html(order):
    out = "<body>"
    out += "<p>Date: " + order.date_ordered.strftime("%A, %B %d, %Y %I:%M%p") + "</p>"
    out += "<p>Job: " + order.job_name + "</p>"
    out += "<p>Employee: " + order.employee_name + "</p>"

    line_items = order.lineitem_set.all()
    if line_items:
        out += "<p>Items</p>"
        out += "<ul>"
        for line_item in line_items:
            out += "<li>" + line_item.item.name + " - " + str(line_item.quantity) + " " + line_item.item.units + "</li>"
        out += "</ul>"

    if order.message:
        out += "<p>" + order.message + "</p>"

    out += "<p>Click <a href='http://localhost:8000/admin/inventory/order/" + str(order.id) + "'>here</a> to view order.</p>"
    out += "</body>"
    return out

def order_to_plaintext(order):
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

    out += "View order: http://localhost:8000/admin/inventory/order/" + str(order.id)
    return out

def email_line(header, data):
    return str(header).title() + ": " + str(data) + "\n"

def string_to_date(date_string):
    date_string = date_string.split("/")
    date_string = [int(x) for x in date_string]
    return date(date_string[2], date_string[0], date_string[1])
