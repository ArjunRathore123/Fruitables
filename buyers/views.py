from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from accounts.models import CustomUser
# Create your views here.

def home(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def registered(request):
    if request.method=='POST':
        email=request.POST['email']
        password1=request.POST['password1'] 
        password2=request.POST['password2']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        gender=request.POST['gender']
        contact=request.POST['contact']
        address=request.POST['address']
        print(gender)
        if password1!=password2:     
            return render(request,'register.html',{'error':'Password and Confirm Password does not match'})
        user=CustomUser.objects.create_user(email=email,password=password1,first_name=first_name,last_name=last_name,gender=gender,contact=contact,address=address)

        user.save()
        
        return render(request,'register.html',{'success':'Account has been created successfully'})
    return render(request,'register.html')

def handlelogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if email and password:
            user=authenticate(request,email=email,password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                messages.success(request,f"You are successfully login")
                return redirect('home')
            else:
                return render(request,'login.html',{'error':'Invalid credentials'})
        else:
            return render(request, 'login.html',{"error":"Email and password are required."} )
    return render(request,'login.html')



def handlelogout(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect('home')