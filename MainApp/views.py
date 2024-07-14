from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *


# Create your views here.
class HomePage(View):
    def get(self,request):
        
        return render(request,'index.html',)

class Jobs(LoginRequiredMixin,View):
    def get(self,request):
        jobs = Job.objects.filter(status = 'open').all()
        context={
                'jobs':jobs
            }
        return render(request,'jobs.html',context)

class Login(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request,'User not found!')
                return render(request, 'login.html')

class Register(View):
    def get(self,request):
        return render(request,'register.html')
    
    def post(self,request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            type = request.POST.get('type')
            try:
                User.objects.get(username = username)
                messages.error(request, 'User already exists, Try logging in!')
                return redirect('/register')
            except Exception as e:
                new_user =  User.objects.create_user(username = username, password=password)
                try:
                    new_user.save()
                    if type == 'driver':
                        new_driver = Driver(user = User.objects.get(username=username))
                        new_driver.save()
                    if type == 'company':
                        new_company = Company(user = User.objects.get(username=username))
                        new_company.save()
                    messages.success(request,'Profile created successfully!')
                    return redirect('/login')
                except Exception as e:
                    messages.error(request,e)
                    return redirect('/register')

def Logout(request):
    logout(request)
    return redirect('/')