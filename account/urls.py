from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('month_selector/<str:button>', views.month_selector, name="month_selector"),
    
    path('bank_detail/', views.bank_detail, name="bank_detail"),
    path('bank/create', views.create_bank_account, name="create_bank_account"),
    path('bank/update/<str:bank_id>', views.update_bank_account, name="update_bank_account"),
    path('bank/remove/<str:bank_id>', views.remove_bank_ac, name="remove_bank_ac"),
]
