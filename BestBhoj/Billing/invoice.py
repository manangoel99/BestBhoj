from InvoiceGenerator.api import Invoice, Client, Provider, Creator, Item
import os
from InvoiceGenerator.pdf import SimpleInvoice
from .models import orders
import datetime

os.environ["INVOICE_LANG"] = "en"

def generate(request, order):
    name = str(order.name)
    phone_number = str(order.phone_number)
    address = str(order.address)
    quantity_60 = int(order.quantity_60)
    quantity_75 = int(order.quantity_75)
    quantity_100 = int(order.quantity_100)
    quantity_125 = int(order.quantity_125)
    quantity_150 = int(order.quantity_150)
    quantity_200 = int(order.quantity_200)
    client = Client(
        summary=name,
        address=address,
        phone=phone_number
        )
    provider = Provider(
        'Best Bhoj', 
        'First Floor, S.C.O-6, Sector-8, Karnal',
        'Karnal',
        '132001'
        )
    creator = Creator(request.user.username)

    invoice = Invoice(client, provider, creator)
    invoice.currency_locale = 'en_US.UTF-8'
    invoice.currency = 'Rs.'
    if quantity_60 > 0:
        invoice.add_item(Item(int(quantity_60), 60, 'Rs 60 Thali'))
    if quantity_75 > 0:
        invoice.add_item(Item(int(quantity_75), 75, 'Rs 75 Thali'))
    if quantity_100 > 0:
        invoice.add_item(Item(int(quantity_100), 100, 'Rs 100 Thali'))
    if quantity_125 > 0:
        invoice.add_item(Item(int(quantity_125), 125, 'Rs 125 Thali'))
    if quantity_150 > 0:
        invoice.add_item(Item(int(quantity_150), 150, 'Rs 150 Thali'))
    if quantity_200 > 0:
        invoice.add_item(Item(int(quantity_200), 200, 'Rs 200 Thali'))

    pdf = SimpleInvoice(invoice)
    try:
        pdf.gen('./Bills/' + name + str(order.pk) + str(datetime.date.today()) + '.pdf')
    except:
        os.system('mkdir ./Bills')
        pdf.gen('./Bills/' + name + str(order.pk) + str(datetime.date.today()) + '.pdf')
