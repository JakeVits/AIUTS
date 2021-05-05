from .models import Account, Transaction
from django.forms import ModelForm
from django import forms


class MyForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['acc_add', 'password', 'balance']


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['sender', 'recipient', 'amount', 'remark']
