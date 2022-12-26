from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import *
from account import utils
import chart.utils as chart_utils

def month_selector(request, button):
    """user selects which month of data to display"""
    month = request.session['display_month']
    year = request.session['display_year']

    if button == 'previous':
        if month > 1:
            month -= 1
        else:
            month = 12
            year -= 1
    elif button == 'next':
        if month < 12:
            month += 1
        else:
            month = 1
            year += 1
    else:
        month, year = button.split(" ")
    
    request.session['display_month'] = month
    request.session['display_year'] = year

    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='/user_login')
def dashboard(request):
    if not request.session.get('display_month') or not request.session.get('display_year'):
        request.session['display_month'] = chart_utils.today.month
        request.session['display_year'] = chart_utils.today.year

    banks = BankAccount.objects.filter(user=request.user)
    net_value = sum(banks.values_list('balance', flat=True))

    selected_month = request.session['display_month']
    selected_year = request.session['display_year']

    income_data_set = utils.main_type_data_set(Income, selected_month, selected_year, request.user)
    expense_data_set = utils.main_type_data_set(Expense, selected_month, selected_year, request.user)
    data_set = [income_data_set, expense_data_set]

    transactions = Transaction.objects.filter(
        date__month=selected_month,
        date__year=selected_year,
        user=request.user
    ).select_related('income', 'expense')

    transactions = [transaction.income if hasattr(transaction, 'income') else transaction.expense for transaction in transactions][:6]

    #transaction count
    transaction_count = income_data_set['transaction_count'] + expense_data_set['transaction_count']

    context = {
        'net_value': net_value,
        'data_set': data_set,
        'transactions': transactions, 
        'transaction_count': transaction_count,
    }

    return render(request, 'dashboard.html', context)


"""bank account related"""
@login_required(login_url='/user_login')
def bank_detail(request):
    form = BankAccountForm()
    banks = BankAccount.objects.filter(user=request.user)

    context = {
        'banks': banks,
        'form': form,
    }
    return render(request, 'bank_detail.html', context)

def create_bank_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            new_bank_ac = form.save(commit=False)
            new_bank_ac.user = request.user
            new_bank_ac.save()
    return redirect('bank_detail')

@login_required(login_url='/user_login')
def update_bank_account(request, bank_id):
    #get the requested object or return none if absence.
    bank = utils.get_object_or_none(model=BankAccount, id=bank_id, user=request.user)

    #return to home if no such object or the user does not own the object
    if (not bank) or (request.user != bank.user):
        return redirect('bank_detail')

    form = BankAccountForm(instance=bank)
    if request.method == 'POST':
        #store the old amount before the form is saved
        old_amount = bank.balance

        #save the form
        form = BankAccountForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()

            #create a transaction named as 'Manual adjustment' 
            #if bank balance is changed
            new_amount = form.cleaned_data['balance']
            if new_amount > old_amount:
                income_adjustment = utils.manual_adjustment(
                    model = Income,
                    date = chart_utils.today,
                    bank = bank,
                    user = request.user,
                )

                income_adjustment.amount += (new_amount - old_amount)
                income_adjustment.save()

            elif new_amount < old_amount:
                expense_adjustment = utils.manual_adjustment(
                    model = Expense,
                    date = chart_utils.today,
                    bank = bank,
                    user = request.user,
                )

                expense_adjustment.amount += (old_amount - new_amount)
                expense_adjustment.save()


        return redirect('bank_detail')

    context = {'form': form}
    return render(request, 'update_bank_account.html', context)   

@login_required(login_url='/user_login')
def remove_bank_ac(request, bank_id):
    #get the requested object or return none if absence.
    bank = utils.get_object_or_none(model=BankAccount, id=bank_id, user=request.user)

    #return to home if no such object or the user does not own the object
    if (not bank) or (request.user != bank.user):
        return redirect('bank_detail')

    bank.delete()
    return redirect('bank_detail')


"""transaction related"""
@login_required(login_url='/user_login')
def transaction_detail(request):
    selected_month = request.session['display_month']
    selected_year = request.session['display_year']

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

def transaction_handler(request, model_form, instance):
    """handle post request in update_transaction"""

    #store the old amount before the form is saved
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

        #change the bank balance if the amount of transaction is changed
        elif new_amount != old_amount:
            changed_amount = new_amount - old_amount
            bank = form.cleaned_data['bank']
            bank.alter_balance(operation='add', nature=instance.nature, 
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
    
    form = transaction_form(instance=transaction, user=request.user)
    if request.method == 'POST':
        return transaction_handler(request, model_form=transaction_form, instance=transaction)

    context = {'form':form}
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

    #deduct the amount from the corresponding bank account.
    amount = transaction.amount
    bank = transaction.bank
    bank.alter_balance(amount=amount, operation='deduct', nature=nature)
    
    transaction.delete()
    return redirect('transaction_detail')


