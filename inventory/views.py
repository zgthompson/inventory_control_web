from django.shortcuts import render

def order(request):
    context = { 'msg': 'hello_world' }
    return render(request, 'inventory/order.html', context)
