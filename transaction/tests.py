from django.test import TestCase
from django.shortcuts import reverse
from .models import Transaction, Account


class TestTransaction(TestCase):

    """ test if 0 or negative amount of loan transfer is accepted """
    def test_negative_amount_of_transaction(self):
        sender = Account.objects.create(acc_add='Jane')
        recipient = Account.objects.create(acc_add='Kate')
        Transaction.objects.create(transaction_id=1, sender=sender, recipient=recipient, amount=100)
        response = self.client.post(reverse('aiuts:transfer', args=['1']), {'sender': sender, 'recipient': recipient,
                                                                            'amount': -100}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Invalid amount of loan for transferring!')

    """ test if above balance of loan transfer is accepted """
    def test_over_balance_amount_of_transaction(self):
        sender = Account.objects.create(acc_add='Jane')
        recipient = Account.objects.create(acc_add='Kate')
        Transaction.objects.create(transaction_id=1, sender=sender, recipient=recipient, amount=100)
        response = self.client.post(reverse('aiuts:transfer', args=['1']), {'sender': sender, 'recipient': recipient,
                                                                            'amount': 1000}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'You do not have enough balance to transfer this amount!')

    """ test if the sender can transfer loan to it's own account """
    def test_transfer_to_herself(self):
        sender = Account.objects.create(acc_add='Jane')
        recipient = Account.objects.create(acc_add='Kate')
        Transaction.objects.create(transaction_id=1, sender=sender, recipient=recipient, amount=100)
        response = self.client.post(reverse('aiuts:transfer', args=['1']), {'sender': sender, 'recipient': sender,
                                                                            'amount': 100}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'You cannot send to your own Account!')


class TestAccount(TestCase):

    """ test if duplicated account address is possible """
    def test_duplicate_account_address(self):
        user1 = self.client.post(reverse('aiuts:form_view'), {'acc_add': 'Jane', 'password': 'hack_jane123',
                                                              'balance': 100}, follow=True)
        user2 = self.client.post(reverse('aiuts:form_view'), {'acc_add': 'Jane', 'password': 'hack_kate123',
                                                              'balance': 100}, follow=True)
        self.assertEquals(user1.status_code, 200)
        self.assertEquals(user2.status_code, 200)
        self.assertContains(user2, 'This Account Exists in the Database Already!')

    """ test if password length can be less than 8 characters """
    def test_password_length(self):
        user = self.client.post(reverse('aiuts:form_view'), {'acc_add': 'Jane', 'password': 'hack',
                                                             'balance': 100}, follow=True)
        self.assertEquals(user.status_code, 200)
        self.assertContains(user, 'Password must have at least 8 characters!')

    """ test if balance providence can be less than $1 """
    def test_balance_providence(self):
        user = self.client.post(reverse('aiuts:form_view'), {'acc_add': 'Jane', 'password': 'hack_jane123',
                                                             'balance': 0}, follow=True)
        self.assertEquals(user.status_code, 200)
        self.assertContains(user, 'Invalid Balance Providence!')

    """ test if credentials meet the requirement of the system """
    def test_credentials(self):
        user = self.client.post(reverse('aiuts:form_view'), {'acc_add': 'Jane', 'password': 'hack_jane123',
                                                             'balance': 100}, follow=True)
        self.assertEquals(user.status_code, 200)
        self.assertContains(user, 'Account Creation Successful!')
