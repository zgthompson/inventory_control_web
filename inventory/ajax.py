from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db.models import Q
from django.core.mail import EmailMessage
import operator
import json
from inventory.models import *

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

    line_items = []
    for key, value in order_data['line_items'].items():
        line_items.append( LineItem(item_id=key, quantity=value['quantity']) )

    order = Order.objects.create()
    order.employee_name = order_data['employee_name']
    order.job_name = order_data['job_name']
    order.message = order_data['message']
    order.lineitem_set.add(*line_items)
    order.save()

    email = EmailMessage('New order', order_to_email(order), to=['zgthompson@gmail.com'])
    email.send()

def email_line(header, data):
    return str(header).title() + ": " + str(data) + "\n"

def order_to_email(order):
    out = "New order\n\n"
    out += email_line("date", order.date_ordered.strftime("%A, %B %d, %Y %I:%M%p"))
    out += email_line("job", order.job_name)
    out += email_line("employee", order.employee_name)
    line_items = order.lineitem_set.all()

    if line_items:
        out += "\nItems\n"
        for line_item in line_items:
            out += email_line(line_item.item.name, line_item.quantity + " " + line_item.units)

    if order.message:
        out += "\nMessage\n" + order.message

    return out

