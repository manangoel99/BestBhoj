from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .models import orders, customers
from .invoice import generate
from .forms import LogInForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
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



#Displaying All Orders 
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



#Displaying Taking Orders Form
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
            order.operator = request.user.username
            order.amount = request.POST['amount']
            order.delivery_boy = request.POST['delivery-boy']
            order.balance = int(request.POST['amount'])
            order.save()
            try:
                x = customers.objects.get(number=order.phone_number)
                print(type(x))
                x.balance += order.balance
                x.save()
            except:
                x = customers()
                x.number = order.phone_number
                x.balance = order.balance
                x.save()
            print(order.date)
            generate(request, order)
            return redirect('all_orders')
        return render(request, 'Billing/takeorder.html')


#Displaying Specific Order Using primary key
@login_required(login_url='/billing')
def spec_order(request, primary_key):
    order = orders.objects.get(pk=primary_key)
    #print(order)
    if request.method == 'POST' and request.user.is_superuser == False:
        if request.POST['payed_amount'] != '':
            order.money_received = request.POST['payed_amount']
            order.balance = request.POST['balance_left']
            order.payment_status = True
            x = customers.objects.get(number=order.phone_number)
            x.balance -= int(order.money_received)
            x.save()
            order.save()
            return redirect('all_orders')
    if request.user.is_superuser and request.method == 'POST':
        #print(request.POST)
        x = customers.objects.get(number=order.phone_number)
        x.balance -= int(order.amount)
        order.quantity_60 = request.POST['60-thali']
        order.quantity_75 = request.POST['75-thali']
        order.quantity_100 = request.POST['100-thali']
        order.quantity_125 = request.POST['125-thali']
        order.quantity_150 = request.POST['150-thali']
        order.quantity_200 = request.POST['200-thali']
        order.address = request.POST['address']
        order.remarks = request.POST['remarks']
        order.amount = request.POST['amount']
        order.balance = int(request.POST['amount'])
        x.balance += int(request.POST['amount'])
        if request.POST['payed_amount'] != '':
            order.money_received = request.POST['payed_amount']
            order.balance = request.POST['balance_left']
            order.payment_status = True
            x.balance -= int(order.money_received)
        order.save()
        x.save()
        return redirect('all_orders')
    if request.user.is_superuser and request.method == 'GET':
        x = customers.objects.get(number=order.phone_number)
        return render(request, 'Billing/mod_order_admin.html', context={
            'customer' : x,
            'order' : order
        })
    if request.user.is_superuser == False and request.method == 'GET':
        x = customers.objects.get(number=order.phone_number)
        return render(request, 'Billing/order_page.html', context={
            'customer' : x,
            'order': order
        })


#Ajax Request Handling
def ajax(request):
    data1 = orders.objects.filter(phone_number=request.GET['phone_number'])
    balace_amount = 0
    for x in data1:
        balace_amount += x.balance
    try:
        data = {
            'balance' : balace_amount,
            'name' : data1[0].name,
            'address' : data1[0].address,
        }
    except:
        data = {
            'balance' : balace_amount
        }
    return JsonResponse(data)
    

#Show All Customers
@login_required(login_url='/billing')
def all_customers(request):
    customers = orders.objects.values('phone_number').all().distinct()
    customer_dict = {}
    for x in customers:
        print(x)
        data = orders.objects.filter(phone_number=x['phone_number'])
        balance = 0
        for z in data:
            balance += z.balance
        customer_dict[x['phone_number']] = balance
    #print(customer_dict)
    return render(request, 'Billing/all_customers.html', context={
        'customer_dict' : customer_dict
    })

#Show Specific Date
@login_required(login_url='/billing')
def dayrec(request):
    if request.method == 'GET':
        return render(request, 'Billing/spec_day_input.html')
    if request.method == 'POST':
        #print(request.POST)
        #print(orders.objects.filter(date=request.POST['DayDate']))
        #return HttpResponse('Hola')
        reqd = orders.objects.filter(date=request.POST['DayDate'])
        tot_money_received = 0
        for order in reqd:
            tot_money_received += order.money_received
        return render(request, 'Billing/spec_day_record.html', context= {
            'orders' : reqd,
            'money_received' : tot_money_received
        })

@login_required(login_url='/billing')
def custompage(request, number):
    order = orders.objects.filter(phone_number=number)
    customer = customers.objects.get(number=number)
    return render(request, 'Billing/custom_orders.html', context={
        'customer' : customer,
        'all_orders' : order
    })

@login_required(login_url='/billing')
def genbill(request, order_num):
    order = orders.objects.get(pk=order_num)
    return render(request, 'Billing/bill_template.html', context={
        'order' : order,
        'price_60' :  60 * order.quantity_60,
        'price_75' :  75 * order.quantity_75,
        'price_100' :  100 * order.quantity_100,
        'price_125' :  125 * order.quantity_125,
        'price_150' :  150 * order.quantity_150,
        'price_200' :  200 * order.quantity_200,
    })

def log_out(request):
    logout(request)
    return redirect(index)
