from django.db import models
from django.contrib.auth.forms import User
from django.utils import timezone
from django.urls import reverse


class Account(models.Model):
    objects = None
    # id = models.AutoField(primary_key=True)
    # username = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.FloatField(default=100.00)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{}".format(self.username)


class Transaction(models.Model):
    objects = None
    transaction_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender', null=True)
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recipient', null=True)
    # sender = models.CharField(max_length=20)
    # recipient = models.CharField(max_length=20)
    amount = models.FloatField()
    remark = models.TextField(max_length=200, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} transferred to {}".format(self.sender, self.recipient)


class PaymentRequest(models.Model):
    objects = None
    request_id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='requester', null=True)
    requested_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='requested_user', null=True)
    request_amount = models.FloatField()
    attachment = models.TextField(max_length=200, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} requested to {}".format(self.requester, self.requested_user)


class DepositRequest(models.Model):
    objects = None
    request_id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='depositor', null=True)
    request_amount = models.FloatField()
    attachment = models.TextField(max_length=200, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Deposit Request From {}'.format(self.requester)
