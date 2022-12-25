from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def user_register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created!")
            return redirect("user_login")
   
    context = {"form": form}
    return render(request, 'user_register.html', context)

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.info(request, "Incorrect username or password.")

    context = {}
    return render(request, 'user_login.html', context)

def user_logout(request):
    logout(request)
    return redirect("dashboard")

def demo_login(request):
    #to login as a demo user
    user = authenticate(request, username='demo_user', password='Demo_User_Password')
    login(request, user)

    return redirect('dashboard')