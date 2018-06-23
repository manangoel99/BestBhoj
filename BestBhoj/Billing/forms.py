from django import forms

class LogInForm(forms.Form):
    username = forms.CharField(label='Enter Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)