from django.db import models
from django.utils import timezone


class Account(models.Model):
    objects = None
    acc_add = models.CharField(max_length=200, primary_key=True, unique=True)
    password = models.CharField(max_length=200, null=False)
    balance = models.FloatField(default=100.00)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{}".format(self.acc_add)


class Transaction(models.Model):
    objects = None
    transaction_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recipient')
    amount = models.FloatField(default=100.00)
    remark = models.TextField(max_length=200, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.sender)
