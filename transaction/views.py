from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
from account.models import Transaction, Expense, Income
from account.forms import IncomeForm, ExpenseForm

from account import utils

"""transaction related"""
@login_required(login_url='/user_login')
def transaction_detail(request):
    selected_month = request.session['display_month']
    selected_year = request.session['display_year']

    #Summary statistics section
    summary_statistics = utils.summary_statistics_data(selected_month, selected_year, request.user)

    income_form = IncomeForm(user=request.user)
    expense_form = ExpenseForm(user=request.user)

    transactions = Transaction.objects.filter(
        date__month=selected_month,
        date__year=selected_year,
        user=request.user
    ).select_related('income', 'expense', 'bank')  #bank name will be used in front-end.

    transactions = [transaction.income if hasattr(transaction, 'income') else transaction.expense for transaction in transactions]
    
    context = {
        'transactions': transactions,
        'income_form': income_form,
        'expense_form': expense_form,
        **summary_statistics
    }
    return render(request, 'transaction_detail.html', context)

def create_transaction(request, nature):
    transaction_form = IncomeForm if nature == 'income' else ExpenseForm
    if request.method == 'POST':
        form = transaction_form(request.user, request.POST)

        if form.is_valid():
            new_instance = form.save(commit=False)
            new_instance.user = request.user
            new_instance.save()

            #change the bank balance
            changed_amount = form.cleaned_data['amount']
            bank = form.cleaned_data['bank']
            bank.alter_balance(operation='add', nature=nature, 
                amount=changed_amount)
            
    return redirect('transaction_detail')

@login_required(login_url='/user_login')
def update_transaction(request, nature, transaction_id):
    transaction_model = Income if nature == 'income' else Expense
    transaction_form = IncomeForm if nature == 'income' else ExpenseForm

    transaction = utils.get_object_or_none(model=transaction_model, id=transaction_id, user=request.user)

    #return to home if no such object or the user does not own the object
    if (not transaction) or (request.user != transaction.user):
        return redirect('transaction_detail')
    
    selected_month = request.session['display_month']
    selected_year = request.session['display_year']
    
    #Summary statistics section
    summary_statistics = utils.summary_statistics_data(selected_month, selected_year, request.user)

    form = transaction_form(instance=transaction, user=request.user)
    if request.method == 'POST':
        return transaction_handler(request, model_form=transaction_form, instance=transaction)

    context = {
        'form':form,
        **summary_statistics
    }
    return render(request, 'update_transaction.html', context)

@login_required(login_url='/user_login')
def remove_transaction(request, nature, transaction_id):
    try:
        transaction = Transaction.objects.select_related('bank').get(id=transaction_id, user=request.user)
    except Transaction.DoesNotExist:
        transaction = None
    
    #return to home if no such object or the user does not own the object
    if (not transaction) or (request.user != transaction.user):
        return redirect('transaction_detail')

    if request.method == 'POST':
        #deduct the amount from the corresponding bank account.
        amount = transaction.amount
        bank = transaction.bank
        bank.alter_balance(amount=amount, operation='deduct', nature=nature)
        
        transaction.delete()
        
    return redirect('transaction_detail')

def transaction_handler(request, model_form, instance):
    """handle POST request in update_transaction."""

    #store some old values before the form is saved
    old_amount = instance.amount
    old_bank = instance.bank

    #save the form
    form = model_form(request.user, request.POST, instance=instance)
    if form.is_valid():
        form.save()

        new_amount = form.cleaned_data['amount']
        new_bank = form.cleaned_data['bank']

        #allocate the bank balance if the bank is changed
        if new_bank != old_bank:
            old_bank.alter_balance(operation='deduct', nature=instance.nature, 
                amount=old_amount)
            new_bank.alter_balance(operation='add', nature=instance.nature, 
                amount=new_amount)

        #change the bank balance if only the amount of transaction is changed
        #elif is used here to eliminate the possibility of changing bank
        elif new_amount != old_amount:
            changed_amount = new_amount - old_amount
            new_bank.alter_balance(operation='add', nature=instance.nature, 
                amount=changed_amount)
            
    return redirect('transaction_detail')
