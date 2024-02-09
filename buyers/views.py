from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from accounts.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
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


def contactus(request):
    return render(request,'contact.html')

def send_email(request):
    if request.method=="POST": 
       email=request.POST['email']
       subject=request.POST['subject']
       name=request.POST.get('name','')
       mobile_number=request.POST.get('number','')
       msg=request.POST['message']
       message=f'Name:{name}\nMobile Number:{mobile_number}\n{email}\n{msg}'
       send_mail(subject,message,email,[settings.EMAIL_HOST_USER],fail_silently=True)
    
       message=f"Hey {name},\nThanks for the enquiry we have received it,\nI am Arjun Rathore. I'm here to welcoming you on behalf of Infograins, I'm a sales director and a founder of Infograins, we will be in touch with you shortly, In a meantime if you have any questions or requirement detail you can revert on this email itself so that based on it we can quickly schedule our discussion or conversation on it.Also, you can schedule a meeting to discuss your specific requirements, here is the calendly link, kindly book your slot as per your convenience, so that we can connect with you to have a more precise conversation regarding your requirement."
       send_mail("Thank you for contact Flipkart",
                 message,
                 settings.EMAIL_HOST_USER,
                 [email],
                 fail_silently=False)

       print(email)

       messages.success(request,"Message sent successfully")
       return render(request,"contactus.html")
    else:
       messages.error(request,"Message not sent ")
       return render(request,"contactus.html")