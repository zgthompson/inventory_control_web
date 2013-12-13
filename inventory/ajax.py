from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from inventory.models import *

@dajaxice_register
def search_items(request, query):
    print query
    dajax = Dajax()

    items = Item.objects.filter(name__icontains=query)

    if items:
        out = ["<table class='table table-striped table-bordered table-hover'><tr><th>Item</th><th>Amount</th><th></th></tr>"]
        for item in items:
            out.append("<tr><td>%s</td><td><input type='text' name='quantity' autocomplete='off' placeholder='0'> %s</td><td><button data='%s' onclick='add_item(this);'>Add</button></td></tr>" % (item.name, item.units, item.id) )
            
        out.append("</table>")
    else:
        out = ["No items found"]
    dajax.assign('#item-results', 'innerHTML', ''.join(out))

    return dajax.json()

