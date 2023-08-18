from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    # check to see if logged in
    if request.method == "POST":
        username = request.POST['username'] # because our form had the name username
        password = request.POST['password']
        # authenticate

        user = authenticate(request, username=username, password=password) # checks if user exists in database
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging in please try again')
            return redirect('home')

    return  render(request, 'home.html', {"records":records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "you have been logged out")
    return redirect('home')

def register_user(request):
    # a doubt i had was how can we block content for both register and home, so it's not that we are rendering base.html and replacing a portion with home.html or base.html, it's that we are rendering home.html or register.html and importing the rest of the stuff from base.html
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username = username, password = password)
            
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'login please!!')
        return redirect('home')
    pass

def delete_record(request, pk): # aslong as I am in delete_record url any post request will be fed to this fucntion
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)

        delete_it.delete()
        messages.success(request, 'record deleted successfully')
        return redirect('home')
    else:
        messages.success(request, 'login please')
        return redirect('home')

def add_record(request):  # aslong as I am in update_record url any post request will be fed to this fucntion
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, 'Please login')
        return redirect('home')

def update_record(request, pk): # aslong as I am in update_record url any post request will be fed to this fucntion
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, 'Please login')
        return redirect('home')