from django.shortcuts import render, redirect

def order(request):
    return render( request, 'inventory/order.html', {} )

def report(request):
    if request.user.is_active and request.user.is_staff:
        return render( request, 'inventory/report.html', {} )
    else:
        return redirect('/admin')

def entry(request):
    if request.user.is_active and request.user.is_staff:
        return render( request, 'inventory/entry.html', {} )
    else:
        return redirect('/admin')

