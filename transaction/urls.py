from django.urls import path
from . import views

urlpatterns = [
    path('transaction_detail/', views.transaction_detail, name="transaction_detail"),
    path('transaction/create/<str:nature>', views.create_transaction, name="create_transaction"),
    path('transaction/update/<str:nature>/<str:transaction_id>', views.update_transaction, name="update_transaction"),
    path('transaction/remove/<str:nature>/<str:transaction_id>', views.remove_transaction, name="remove_transaction"),

]
