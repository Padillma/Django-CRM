from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()
    #check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Success! You have been logged in.")
            return redirect('home')
        else:
            messages.success(request, "Oh no.. There seems to been an error logging in.")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

""" commented this out because i am adding a login form in the homepage instead
def login_user(request):
    pass
"""

def about(request):
     return render(request, 'about.html',{})

def contact(request):
     return render(request, 'contact.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out..")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authicate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
        """else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += 'form-control border-danger' """
                
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        #look up records for users
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    
    else:
        messages.success(request, "You must be logged in to access the page information..")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully..")
        return redirect('home')
    else:
        messages.success(request, "Error... You must be logged in..")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                
            # Create, but don't save the new author instance.
                employee = form.save(commit=False)
                user_id = request.user.id
                employee.emp_id = user_id
                form.save()
                messages.success(request, "Record Added")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "Error... You must be logged in..")
        return redirect('home')
    
def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "Error... You must be logged in..")
		return redirect('home')