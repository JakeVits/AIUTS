from .models import Account, Transaction
from .forms import MyForm, TransactionForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
import hashlib


class FormPage(generic.CreateView):
    template_name = 'transaction/account_form.html'
    form_class = MyForm
    success_url = reverse_lazy('aiuts:list_view')
    instance = ''

    def form_valid(self, form):
        self.instance = form.save(commit=False)  # get model object
        hashed_acc = hashlib.md5(form.cleaned_data['acc_add'].encode("utf-8")).hexdigest()
        hashed_pass = hashlib.md5(form.cleaned_data['password'].encode("utf-8")).hexdigest()
        duplicate_acc_add = Account.objects.filter(acc_add=hashed_acc)
        if duplicate_acc_add:
            messages.info(self.request, 'This Account Exists in the Database Already!')
            return super(FormPage, self).form_invalid(form)
        elif len(form.cleaned_data['password']) < 8:
            messages.info(self.request, 'Password must have at least 8 characters!')
            return super(FormPage, self).form_invalid(form)
        elif form.cleaned_data['balance'] < 1:
            messages.info(self.request, 'Invalid Balance Providence!')
            return super(FormPage, self).form_invalid(form)
        else:
            messages.success(self.request, 'Account Creation Successful!')
            self.instance.acc_add = hashed_acc
            self.instance.password = hashed_pass
            form.save()
            return super(FormPage, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request, 'Credentials cannot be Emptied!')
        return super(FormPage, self).form_invalid(form)


class ListPage(generic.ListView):
    template_name = 'transaction/account_list.html'
    queryset = Account.objects.all()
    # context_object_name = 'account_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['account_list'] = Account.objects.all().order_by('-created_at')
        return context


class DashboardView(generic.DetailView):
    template_name = 'transaction/dashboard.html'

    def get_queryset(self):
        return Account.objects.filter(pk=self.kwargs['pk'])


class UserDetailsView(generic.DetailView):
    template_name = 'transaction/detail.html'

    def get_queryset(self):
        return Account.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['detail_list'] = self.get_queryset()
        return context


class HistoryView(generic.ListView):
    template_name = 'transaction/transaction_history.html'

    def get_queryset(self):
        return Transaction.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['history_list'] = Transaction.objects.filter(sender=self.kwargs['pk']).order_by('-transaction_date')
        return context


class TransactionFormView(generic.CreateView):
    form_class = TransactionForm
    template_name = 'transaction/transaction_form.html'

    def get_queryset(self):
        return Account.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_user'] = self.get_queryset()
        context['user_list'] = Account.objects.exclude(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('aiuts:transfer', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        sender = Account.objects.get(acc_add=self.request.POST.get('sender'))
        recipient = Account.objects.get(acc_add=self.request.POST.get('recipient'))
        transaction_amount = form.cleaned_data['amount']

        ''' transaction operations are done here '''
        if sender == recipient:
            messages.error(self.request, 'You cannot send to your own Account!')
            return super(TransactionFormView, self).form_invalid(form)
        if transaction_amount < 1:
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

