from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import *
from .utils import main_type_data_set, displayed_month, get_object_or_none


def month_selector(request, selected_month):
    """user selects which month of data to display"""
    request.session['display_month'] = selected_month
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='/user_login')
def dashboard(request):
    selected_month = displayed_month(request)
    
    banks = BankAccount.objects.filter(user=request.user)
    net_value = sum(banks.values_list('total_amount', flat=True))

    income_data_set = main_type_data_set(Income, selected_month)
    expense_data_set = main_type_data_set(Expense, selected_month)
    data_set = [income_data_set, expense_data_set]

    transactions = Transaction.objects.filter(date__month=selected_month).select_related('income', 'expense')
    transactions = [transaction.income if hasattr(transaction, 'income') else transaction.expense for transaction in transactions][:6]

    #transaction count
    transaction_count = income_data_set['transaction_count'] + income_data_set['transaction_count']

    context = {
        'banks': banks, 
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

def update_bank_account(request, bank_id):
    #get the requested object or return none if absence.
    bank = get_object_or_none(model=BankAccount, id=bank_id, user=request.user)

    #return to home if no such object or the user does not own the object
    if (not bank) or (request.user != bank.user):
        return redirect('bank_detail')

    form = BankAccountForm(instance=bank)
    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
        return redirect('bank_detail')

    context = {'form': form}
    return render(request, 'update_bank_account.html', context)   

def remove_bank_ac(request, bank_id):
    #get the requested object or return none if absence.
    bank = get_object_or_none(model=BankAccount, id=bank_id, user=request.user)

    #return to home if no such object or the user does not own the object
    if (not bank) or (request.user != bank.user):
        return redirect('bank_detail')

    bank.delete()
    return redirect('bank_detail')


"""transaction related"""
@login_required(login_url='/user_login')
def transaction_detail(request):
    selected_month = displayed_month(request)

    income_form = IncomeForm()
    expense_form = ExpenseForm()

    transactions = Transaction.objects.filter(date__month=selected_month).select_related('income', 'expense')
    transactions = [transaction.income if hasattr(transaction, 'income') else transaction.expense for transaction in transactions]
    
    context = {
        'transactions': transactions,
        'income_form':income_form,
        'expense_form':expense_form,
    }
    return render(request, 'transaction_detail.html', context)

def create_transaction(request, nature):
    transaction_form = IncomeForm if nature == 'income' else ExpenseForm
    if request.method == 'POST':
        form = transaction_form(request.POST)

        if form.is_valid():
            new_instance = form.save(commit=False)
            new_instance.user = request.user
            new_instance.save()

            #change the bank balance, send signal to bank_ac model?
            changed_amount = form.cleaned_data['amount']
            bank = form.cleaned_data['bank']
            bank.alter_balance(operation='add', nature=nature, 
                amount=changed_amount)
            
    return redirect('transaction_detail')

def transaction_handler(request, model_form, instance):
    """handle post request in update_transaction"""

    #store the old amount before the form is saved
    old_amount = instance.amount

    #save the form
    form = model_form(request.POST, instance=instance)
    if form.is_valid():
        form.save()

        #change the bank balance if the amount of transaction is changed
        new_amount = form.cleaned_data['amount']
        if new_amount != old_amount:
            changed_amount = new_amount - old_amount
            bank = form.cleaned_data['bank']
            bank.alter_balance(operation='add', nature=instance.nature, 
                amount=changed_amount)
            
    return redirect('transaction_detail')
   
def update_transaction(request, nature, transaction_id):
    transaction_model = Income if nature == 'income' else Expense
    transaction_form = IncomeForm if nature == 'income' else ExpenseForm

    transaction = get_object_or_none(model=transaction_model, id=transaction_id, user=request.user)

    #return to home if no such object or the user does not own the object
    if (not transaction) or (request.user != transaction.user):
        return redirect('transaction_detail')
    
    form = transaction_form(instance=transaction)
    if request.method == 'POST':
        return transaction_handler(request, model_form=transaction_form, instance=transaction)

    context = {'form':form}
    return render(request, 'update_transaction.html', context)

def remove_transaction(request, nature, transaction_id):
    try:
        transaction = Transaction.objects.select_related('bank').get(id=transaction_id, user=request.user)
    except Transaction.DoesNotExist or Transaction.MultipleObjectsReturned:
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


"""useless"""
def category_detail(request, category):
    transactions = Transaction.objects.filter(category=category)
    sub_total = sum(transactions.values_list('amount', flat=True))

    context = {'transactions': transactions, 'sub_total': sub_total}
    return render(request, 'detail_page.html', context)

def main_type_detail(request, nature):
    if nature =='income':
        tran_model = Income
    else:
        tran_model = Expense

    transactions = tran_model.objects.all()
    sub_total = sum(transactions.values_list('amount', flat=True))

    context = {'transactions': transactions, 'sub_total': sub_total}
    return render(request, 'detail_page.html', context)


    
 
"""  use a bootstrap model to render the category button, or customize one.
 if customize, category/custom
 form = customform()
 cate = form.save(commit=False)
 cate.user = request.user
 return redirect('/category/' + str(cate.category))
 
 if choose one: category/<cate:str>   
 form = tranform()
 tranform(reuqest.POST), tran = form.save(commit=False)
 tran.cate = cate  """
    
#transaction filter according to income/expense/internal transfer?