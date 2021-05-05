from django.urls import path
from . import views

app_name = 'aiuts'
urlpatterns = [
    path('', views.ListPage.as_view(), name="list_view"),
    path('form', views.FormPage.as_view(), name="form_view"),
    path('transfer/<pk>/', views.TransactionFormView.as_view(), name="transfer"),
    path('dashboard/<pk>/', views.DashboardView.as_view(), name="dashboard"),
    path('details/<pk>/', views.UserDetailsView.as_view(), name="details"),
    path('history/<pk>/', views.HistoryView.as_view(), name="history"),
]
