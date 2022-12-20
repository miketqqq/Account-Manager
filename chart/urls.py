from django.urls import path
from . import views

urlpatterns = [
    path('income_expense_chart', views.income_expense_chart, name="income_expense_chart"),
    path('bank_account_chart', views.bank_account_chart, name="bank_account_chart"),
    path('category_chart', views.category_chart, name="category_chart"),

]
