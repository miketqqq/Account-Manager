from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('month_selector/<str:button>', views.month_selector, name="month_selector"),
    
    path('bank_detail/', views.bank_detail, name="bank_detail"),
    path('create_bank_account/', views.create_bank_account, name="create_bank_account"),
    path('update_bank_account/<str:bank_id>', views.update_bank_account, name="update_bank_account"),
    path('remove_bank_ac/<str:bank_id>', views.remove_bank_ac, name="remove_bank_ac"),

    path('transaction_detail/', views.transaction_detail, name="transaction_detail"),
    path('create_transaction/<str:nature>', views.create_transaction, name="create_transaction"),
    path('update_transaction/<str:nature>/<str:transaction_id>', views.update_transaction, name="update_transaction"),
    path('remove_transaction/<str:nature>/<str:transaction_id>', views.remove_transaction, name="remove_transaction"),

]
