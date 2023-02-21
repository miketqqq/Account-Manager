from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from account.models import BankAccount, Transaction, Expense, Income
from account.forms import BankAccountForm

from account import utils
from account.constant import TODAY
from functools import partial


@login_required(login_url='/user_login')
def dashboard(request):
    if not request.session.get('display_month') or not request.session.get('display_year'):
        request.session['display_month'] = TODAY.month
        request.session['display_year'] = TODAY.year

    selected_month = request.session['display_month']
    selected_year = request.session['display_year']
    
    #Summary statistics section
    summary_statistics = utils.summary_statistics_data(selected_month, selected_year, request.user)

    #Recent Transactions section
    transactions = Transaction.objects.filter(
        date__month=selected_month,
        date__year=selected_year,
        user=request.user
    ).select_related('income', 'expense', 'bank')
    
    transactions = [
        transaction.income if hasattr(transaction, 'income') else transaction.expense for transaction in transactions
    ][:6]

    context = {
        'transactions': transactions, 
        **summary_statistics,
    }

    return render(request, 'dashboard.html', context)

def month_selector(request, button):
    """user selects which month of data to display."""
    month = int(request.session['display_month'])
    year = int(request.session['display_year'])

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
    elif button == 'select':
        year, month = request.GET.get('year-month').split("-")
    
    request.session['display_month'] = int(month)
    request.session['display_year'] = int(year)

    return redirect(request.META['HTTP_REFERER'])



"""bank account related"""
@login_required(login_url='/user_login')
def bank_detail(request):
    form = BankAccountForm()
    banks = BankAccount.objects.filter(user=request.user)

    selected_month = request.session['display_month']
    selected_year = request.session['display_year']
    
    #Summary statistics section
    summary_statistics = utils.summary_statistics_data(selected_month, selected_year, request.user)

    context = {
        'banks': banks,
        'form': form,
        **summary_statistics
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

    selected_month = request.session['display_month']
    selected_year = request.session['display_year']
    
    #Summary statistics section
    summary_statistics = utils.summary_statistics_data(selected_month, selected_year, request.user)

    form = BankAccountForm(instance=bank)
    if request.method == 'POST':
        #store the old amount before the form is saved
        old_amount = bank.balance

        #save the form
        form = BankAccountForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()

            #create a transaction named as 'Manual adjustment' 
            #if bank balance is changed by user
            new_amount = form.cleaned_data['balance']
            partial_manual_adjustment = partial(utils.manual_adjustment,
                bank = bank,
                user = request.user)

            if new_amount > old_amount:
                income_adjustment = partial_manual_adjustment(model=Income)
                income_adjustment.amount += (new_amount - old_amount)
                income_adjustment.save()

            elif new_amount < old_amount:
                expense_adjustment = partial_manual_adjustment(model=Expense)
                expense_adjustment.amount += (old_amount - new_amount)
                expense_adjustment.save()

        return redirect('bank_detail')

    context = {
        'form': form,
        **summary_statistics
    }
    return render(request, 'update_bank_account.html', context)   

@login_required(login_url='/user_login')
def remove_bank_ac(request, bank_id):
    #get the requested object or return none if absence.
    bank = utils.get_object_or_none(model=BankAccount, id=bank_id, user=request.user)

    #return to home if no such object or the user does not own the object
    if (not bank) or (request.user != bank.user):
        return redirect('bank_detail')

    if request.method == 'POST':
        bank.delete()

    return redirect('bank_detail')


