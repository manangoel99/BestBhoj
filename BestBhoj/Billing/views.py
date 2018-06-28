from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import orders
from .forms import LogInForm


# Create your views here.
def index(request):
    #context = {}
    #return render(request, 'Billing/index.html', context)
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            #return HttpResponse("Thanks")
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                all_orders = orders.objects.all()
                context = {
                    'all _ orders' : all_orders
                }
                return redirect(order_display)
            else:
                form = LogInForm()
    else:
        form = LogInForm()
    return render(request, 'Billing/index.html', {
        'form' : form
        })

@login_required(login_url='/billing')
def order_display(request):
    print(request.user)
    if request.user.is_authenticated:
        print(request.user)
        all_orders = orders.objects.all()
        context = {
            'all_orders': all_orders,
            'user' : request.user
        }
        return render(request, 'Billing/all_orders.html', context=context)
    else:
        return redirect(index)

@login_required(login_url='/billing')
def take_order(request):
    if request.user.is_authenticated:
        print(request.user)
        #print(request.method)
        if request.method == 'POST':
            order = orders()
            order.name = request.POST['name']
            order.phone_number = request.POST['number']
            order.quantity_60 = request.POST['60-thali']
            order.quantity_75 = request.POST['75-thali']
            order.quantity_100 = request.POST['100-thali']
            order.quantity_125 = request.POST['125-thali']
            order.quantity_150 = request.POST['150-thali']
            order.quantity_200 = request.POST['200-thali']
            order.address = request.POST['address']
            order.remarks = request.POST['remarks']
            order.operator = request.user
            order.amount = request.POST['amount']
            order.delivery_boy = request.POST['delivery-boy']
            order.save()
            return redirect('all_orders')
        return render(request, 'Billing/takeorder.html')
    

def log_out(request):
    logout(request)
    return redirect(index)
