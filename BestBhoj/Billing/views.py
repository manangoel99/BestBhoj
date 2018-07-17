from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import xlrd

from .models import orders, customers, menu
from .forms import LogInForm

def read_menu():
    menu.objects.all().delete()
    wb = xlrd.open_workbook('Billing/menu.xls')
    sheet = wb.sheet_by_index(0)

    for i in range(1, sheet.nrows):
        item = menu()
        item.item = sheet.cell_value(i, 1)
        item.price = round(float(sheet.cell_value(i, 8)))
        item.save()
        print(sheet.cell_value(i, 1), round(float(sheet.cell_value(i, 8))))

    

# Create your views here.
def status_change(request):
    order = orders.objects.get(pk=int(request.POST['order_id']))
    order.delivery_boy = request.POST['delivery_boy']
    order.delivery_status = True
    order.save()

def get_undelivered():
    return orders.objects.filter(delivery_status=False)

def index(request):
    read_menu()
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
    if request.user.is_authenticated:
        if request.method == 'POST' and 'status_change' in request.POST:
            print(request.POST)
            status_change(request)
        all_orders = orders.objects.all()
        context = {
            'all_orders': all_orders,
            'user' : request.user,
            'undelivered' : get_undelivered()
        }
        return render(request, 'Billing/all_orders.html', context=context)
    else:
        return redirect(index)



#Displaying Taking Orders Form
@login_required(login_url='/billing')
def take_order(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'status_change' in request.POST:
                status_change(request)
            else:
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
                    x.balance += order.balance
                    x.save()
                except:
                    x = customers()
                    x.number = order.phone_number
                    x.balance = order.balance
                    x.save()
                return redirect('all_orders')
        return render(request, 'Billing/takeorder.html', context={
            'undelivered': get_undelivered()
        })


#Displaying Specific Order Using primary key
@login_required(login_url='/billing')
def spec_order(request, primary_key):
    order = orders.objects.get(pk=primary_key)
    if request.method == 'POST' and 'status_change' in request.POST:
        print(request.POST)
        status_change(request)
        if request.user.is_superuser:
            x = customers.objects.get(number=order.phone_number)
            return render(request, 'Billing/mod_order_admin.html', context={
                'customer': x,
                'order': order,
                'undelivered': get_undelivered()
            })
        else:
            x = customers.objects.get(number=order.phone_number)
            return render(request, 'Billing/order_page.html', context={
                'customer': x,
                'order': order,
                'undelivered': get_undelivered()
            })
    if request.method == 'POST' and request.user.is_superuser == False and 'status_change' not in request.POST:
        if request.POST['payed_amount'] != '':
            order.money_received = request.POST['payed_amount']
            order.balance = request.POST['balance_left']
            order.payment_status = True
            x = customers.objects.get(number=order.phone_number)
            x.balance -= int(order.money_received)
            x.save()
            order.save()
            return redirect('all_orders')
    if request.user.is_superuser and request.method == 'POST' and 'status_change' not in request.POST:
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
            'order' : order,
            'undelivered': get_undelivered()
        })
    if request.user.is_superuser == False and request.method == 'GET':
        x = customers.objects.get(number=order.phone_number)
        return render(request, 'Billing/order_page.html', context={
            'customer' : x,
            'order': order, 
            'undelivered': get_undelivered()
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
    if request.method == 'POST':
        if 'status_change' in request.POST:
            print(request.POST)
            status_change(request)
    customers = orders.objects.values('phone_number').all().distinct()
    customer_dict = {}
    for x in customers:
        print(x)
        data = orders.objects.filter(phone_number=x['phone_number'])
        balance = 0
        for z in data:
            balance += z.balance
        customer_dict[x['phone_number']] = balance
    return render(request, 'Billing/all_customers.html', context={
        'customer_dict' : customer_dict,
        'undelivered': get_undelivered()
    })

#Show Specific Date
@login_required(login_url='/billing')
def dayrec(request):
    if request.method == 'GET':
        return render(request, 'Billing/spec_day_input.html', context={
            'undelivered': get_undelivered()
        })
    if request.method == 'POST':
        reqd = orders.objects.filter(date=request.POST['DayDate'])
        tot_money_received = 0
        for order in reqd:
            tot_money_received += order.money_received
        return render(request, 'Billing/spec_day_record.html', context= {
            'orders' : reqd,
            'money_received' : tot_money_received,
            'undelivered': get_undelivered()
        })
    
@login_required(login_url='/billing')
def custompage(request, number):
    if request.method == 'POST' and 'status_change' in request.POST:
        print(request.POST)
        status_change(request)
    order = orders.objects.filter(phone_number=number)
    customer = customers.objects.get(number=number)
    return render(request, 'Billing/custom_orders.html', context={
        'customer' : customer,
        'all_orders' : order,
        'undelivered': get_undelivered()
    })

@login_required(login_url='/billing')
def genbill(request, order_num):
    order = orders.objects.get(pk=order_num)
    customer = customers.objects.get(number=order.phone_number)
    return render(request, 'Billing/bill_template.html', context={
        'order' : order,
        'price_60' :  60 * order.quantity_60,
        'price_75' :  75 * order.quantity_75,
        'price_100' :  100 * order.quantity_100,
        'price_125' :  125 * order.quantity_125,
        'price_150' :  150 * order.quantity_150,
        'price_200' :  200 * order.quantity_200,
        'customer' : customer,
    })

def log_out(request):
    logout(request)
    return redirect(index)
