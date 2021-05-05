from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, TransactionForm, PaymentRequestForm, DepositRequestForm
from .models import Account, User, PaymentRequest, Transaction, DepositRequest


class RegistrationPage(generic.CreateView):
    template_name = 'transaction_secondchallenge/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('transaction:dashboard')

    def form_valid(self, form):
        valid = super(RegistrationPage, self).form_valid(form)
        user = User.objects.get(username=form.cleaned_data['username'])
        username = Account(username=user)
        username.save()
        user = authenticate(self.request, username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
            return valid
        else:
            messages.warning(self.request, 'Invalid Authentication!')
            return super().form_invalid(form)


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'transaction_secondchallenge/dashboard.html'
    login_url = '/accounts/login/'


class UserDetailsView(LoginRequiredMixin, generic.DetailView):
    template_name = 'transaction_secondchallenge/detail.html'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return Account.objects.filter(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['detail_list'] = self.get_queryset()
        return context


class HistoryView(generic.ListView):
    template_name = 'transaction_secondchallenge/transaction_history.html'

    def get_queryset(self):
        return User.objects.get(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        current_user = Account.objects.get(username=self.get_queryset())
        context['history_list'] = Transaction.objects.filter(sender=current_user).order_by('-transaction_date')
        return context


class NotificationView(generic.ListView):
    login_url = '/accounts/login/'
    template_name = 'transaction_secondchallenge/notification.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return DepositRequest.objects.all().order_by('-request_date')
        else:
            return PaymentRequest.objects.filter(requested_user=
                                                 Account.objects.get(username=self.request.user)).order_by('-request_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['noty_details'] = self.get_queryset()
        return context


class ApprovalView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/accounts/login/'
    fields = '__all__'

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.filter(username=self.request.user)
        else:
            return Account.objects.all()

    def get_success_url(self):
        return reverse_lazy('transaction:notification', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        if self.request.user.is_staff:
            requester = Account.objects.get(username=User.objects.get(username=self.request.POST.get('requester')))
            amount = float(self.request.POST.get('request_amount'))
            request_id = DepositRequest.objects.get(request_id=self.request.POST.get('id'))
            requester.balance = requester.balance + amount
            requester.save()
            request_id.delete()
            messages.success(self.request, 'Deposit Request is Approved and Transacted Successful!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            requester = Account.objects.get(username=User.objects.get(username=self.request.POST.get('requester')))
            requested_user = Account.objects.get(username=self.request.user)
            request_id = PaymentRequest.objects.get(request_id=self.request.POST.get('id'))
            amount = float(self.request.POST.get('request_amount'))
            if requested_user.balance - amount > 0:
                requester.balance = requester.balance + amount
                requested_user.balance = requested_user.balance - amount
                requester.save()  # saving requester balance in Account model
                requested_user.save()  # saving requested user/current user balance in Account model
                Transaction(sender=requested_user, recipient=requester, amount=amount).save()
                request_id.delete()
                messages.success(self.request, 'Loan is Approved and Transacted Successful!')
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.error(self.request, 'You do not have enough balance to approve this amount!')
                return HttpResponseRedirect(self.get_success_url())


class NegotiateFormView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/accounts/login/'
    template_name = 'transaction_secondchallenge/negotiation_form.html'
    model = Account
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['request_id'] = self.request.POST.get('id')
        context['requester'] = self.request.POST.get('requester')
        return context


class NegotiateView(generic.UpdateView):
    login_url = '/accounts/login/'
    template_name = 'transaction_secondchallenge/transaction_form.html'
    model = Account
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('transaction:notification', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        requester = Account.objects.get(username=User.objects.get(username=self.request.POST.get('requester')))
        requested_user = Account.objects.get(username=self.request.user)
        request_id = PaymentRequest.objects.get(request_id=self.request.POST.get('id'))
        amount = float(self.request.POST.get('request_amount'))
        if requested_user.balance - amount > 0:
            requester.balance = requester.balance + amount
            requested_user.balance = requested_user.balance - amount
            requester.save()  # saving requester balance in Account model
            requested_user.save()  # saving requested user/current user balance in Account model
            Transaction(sender=requested_user, recipient=requester, amount=amount).save()
            request_id.delete()
            messages.success(self.request, 'Loan is Negotiated and Transacted Successful!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'You do not have Enough Balance to Negotiate this Amount!')
            return HttpResponseRedirect(self.get_success_url())


class DeclineView(generic.DeleteView):
    login_url = '/accounts/login/'
    template_name = 'transaction_secondchallenge/notification.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return DepositRequest.objects.all()
        else:
            return PaymentRequest.objects.all()

    def get_success_url(self):
        if self.request.user.is_staff:
            messages.info(self.request, "Successfully Declined!")
            return reverse_lazy('transaction:notification', kwargs={'pk': self.object.pk})
        else:
            messages.info(self.request, "Don't worry we will not tell the requester that you declined!")
            return reverse_lazy('transaction:notification', kwargs={'pk': self.object.pk})


class PaymentRequestView(LoginRequiredMixin, generic.CreateView):
    template_name = 'transaction_secondchallenge/payment_request.html'
    form_class = PaymentRequestForm
    login_url = '/accounts/login/'
    success_url = reverse_lazy('transaction:request_amount')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super(PaymentRequestView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        requester = Account.objects.get(username=form.cleaned_data['requester'])
        requested_user = Account.objects.get(username=form.cleaned_data['requested_user'])
        requested_amount = form.cleaned_data['request_amount']

        if requester == requested_user:
            messages.error(self.request, 'You cannot request to your own account!')
            return super(PaymentRequestView, self).form_invalid(form)
        elif requested_amount < 1:
            messages.error(self.request, 'Invalid amount of loan request!')
            return super(PaymentRequestView, self).form_invalid(form)
        else:
            requester.save()
            requested_user.save()
            messages.success(self.request, 'Loan Request Successful!')
            return super(PaymentRequestView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Loan Request!')
        return super(PaymentRequestView, self).form_invalid(form)


class DepositRequestView(LoginRequiredMixin, generic.CreateView):
    template_name = 'transaction_secondchallenge/deposit_request.html'
    form_class = DepositRequestForm
    login_url = '/accounts/login/'
    success_url = reverse_lazy('transaction:deposit')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super(DepositRequestView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Deposit Request Successful!')
        return super(DepositRequestView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error Request!')
        return super(DepositRequestView, self).form_invalid(form)


class TransactionFormView(LoginRequiredMixin, generic.CreateView):
    form_class = TransactionForm
    template_name = 'transaction_secondchallenge/transaction_form.html'
    login_url = '/accounts/login/'
    success_url = reverse_lazy('transaction:transfer')

    def get_queryset(self):
        return Account.objects.filter(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_user_balance'] = self.get_queryset()
        return context

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super(TransactionFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        sender = Account.objects.get(username=User.objects.get(username=self.request.user))
        recipient = Account.objects.get(username=User.objects.get(username=form.cleaned_data['recipient']))
        transaction_amount = form.cleaned_data['amount']

        ''' transaction operations are done here '''
        if sender == recipient:
            messages.error(self.request, 'You cannot send to your own Account!')
            return super(TransactionFormView, self).form_invalid(form)
        elif transaction_amount < 1:
            messages.error(self.request, 'Invalid amount of loan for transferring!')
            return super(TransactionFormView, self).form_invalid(form)
        elif transaction_amount > sender.balance or sender.balance <= 0:
            messages.error(self.request, 'You do not have enough balance to transfer this amount!')
            return super(TransactionFormView, self).form_invalid(form)
        else:
            sender.balance = sender.balance - transaction_amount
            recipient.balance = recipient.balance + transaction_amount
            sender.save()
            recipient.save()
            messages.success(self.request, 'Loan Transaction Successful!')
            return super(TransactionFormView, self).form_valid(form)
