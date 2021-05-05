from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.forms import ModelForm
from .models import Transaction, PaymentRequest, Account, DepositRequest
from django.core.exceptions import ObjectDoesNotExist
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None


class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['sender', 'recipient', 'amount', 'remark']

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user are given as options"""
        self.request = kwargs.pop('request')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['sender'].queryset = Account.objects.filter(username=self.request.user)
        self.fields['sender'].empty_label = None
        self.fields['recipient'].queryset = Account.objects.exclude(username=self.request.user)


class PaymentRequestForm(ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['requester', 'requested_user', 'request_amount', 'attachment']

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user are given as options"""
        self.request = kwargs.pop('request')
        super(PaymentRequestForm, self).__init__(*args, **kwargs)
        self.fields['requester'].queryset = Account.objects.filter(username=self.request.user)
        self.fields['requester'].empty_label = None
        self.fields['requested_user'].queryset = Account.objects.exclude(username=self.request.user)


class DepositRequestForm(ModelForm):
    class Meta:
        model = DepositRequest
        fields = ['requester', 'request_amount', 'attachment']

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user are given as options"""
        self.request = kwargs.pop('request')
        super(DepositRequestForm, self).__init__(*args, **kwargs)
        self.fields['requester'].queryset = Account.objects.filter(username=self.request.user)
        self.fields['requester'].empty_label = None
