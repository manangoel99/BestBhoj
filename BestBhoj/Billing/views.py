from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .models import orders
from .forms import LogInForm
import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice

os.environ['INVOICE_LANG'] = "en"
OFFICE_ADDRESS = 'First Floor, S.C.O-6, Sector-8, Karnal'

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
            order.operator = request.user
            order.amount = request.POST['amount']
            order.delivery_boy = request.POST['delivery-boy']
            client = Client(request.POST['name'], request.POST['address'], phone=request.POST['number'])
            provider = Provider('Best Bhoj',OFFICE_ADDRESS,'Karnal', phone='')
            creator = Creator(request.user)
            invoice = Invoice(client, provider, creator)
            invoice.add_item(Item(request.POST['60-thali'], 60, 'Rs. 60 Thali'))
            invoice.add_item(Item(request.POST['75-thali'], 75, 'Rs. 75 Thali'))
            invoice.add_item(Item(request.POST['100-thali'], 100, 'Rs. 100 Thali'))
            invoice.add_item(Item(request.POST['125-thali'], 125, 'Rs. 125 Thali'))
            invoice.add_item(Item(request.POST['150-thali'], 150, 'Rs. 150 Thali'))
            invoice.add_item(Item(request.POST['200-thali'], 200, 'Rs. 200 Thali'))
            pdf = SimpleInvoice(invoice)
            print(type(order.pk))
            pdf.gen('../' + str(request.POST['name']) + '.pdf', generate_qr_code=False)
            order.save()
            return redirect('all_orders')
        return render(request, 'Billing/takeorder.html')


#Displaying Specific Order Using primary key
@login_required(login_url='/billing')
def spec_order(request, primary_key):
    order = orders.objects.get(pk=primary_key)
    #print(order)
    if request.method == 'POST':
        if request.POST['payed_amount'] != '':
            order.money_received = request.POST['payed_amount']
            order.balance = request.POST['balance_left']
            order.payment_status = True
            order.save()
            return redirect('all_orders')
    return render(request, 'Billing/order_page.html', context={
        'order' : order
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

def log_out(request):
    logout(request)
    return redirect(index)
