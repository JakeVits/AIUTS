from django.urls import path
from . import views

app_name = 'transaction'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('registration', views.RegistrationPage.as_view(), name='registration'),
    # path('logout', views.LogoutView.as_view(), name='logout'),
    path('details/<pk>', views.UserDetailsView.as_view(), name='details'),
    path('request-amount', views.PaymentRequestView.as_view(), name='request_amount'),
    path('transfer', views.TransactionFormView.as_view(), name='transfer'),
    path('deposit', views.DepositRequestView.as_view(), name='deposit'),
    path('negotiate_form/<pk>', views.NegotiateFormView.as_view(), name='negotiate_form'),
    path('negotiate/<pk>', views.NegotiateView.as_view(), name='negotiate'),
    path('approval/<pk>', views.ApprovalView.as_view(), name='approval'),
    path('decline/<pk>', views.DeclineView.as_view(), name='decline'),
    path('notification/<pk>', views.NotificationView.as_view(), name='notification'),
    path('history', views.HistoryView.as_view(), name='history')
]
