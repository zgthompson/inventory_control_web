from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def assign_test(request):
    dajax = Dajax()
    dajax.assign('#box', 'innerHTML', 'Hello World!')
    return dajax.json()

