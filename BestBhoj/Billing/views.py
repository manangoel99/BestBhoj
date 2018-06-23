from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

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
                return HttpResponse("<h1>Thanks For Logging In</h1>")
            else:
                form = LogInForm()
    else:
        form = LogInForm()
    return render(request, 'Billing/index.html', {
        'form' : form
        })
