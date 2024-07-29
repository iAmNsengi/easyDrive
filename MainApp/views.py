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
    
class AddJob(LoginRequiredMixin,View):
    def get(self,request):
        return render(request, 'add_job.html')
    
    def post(self,request):
        title = request.POST.get('title')
        job_type = request.POST.get('job-type')
        location = request.POST.get('location')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')

        try:
            new_job = Job(creator = User.objects.get(username = request.user), title =title,location=location,description=description,requirements=requirements,type=job_type )
            new_job.save()
            messages.success(request,'Job added successfully!')
            return redirect('/add_job')
        
        except Exception as e:
            messages.error(request,e)
            return redirect('/add_job')


class JobDetail(LoginRequiredMixin,View):
    def get(self, request,id):
        context = {}
        try:
            job = Job.objects.get(id=id)
            context = {
                'job':job
            }
        except Exception as e:
            messages.error(request,e)
            return redirect('/jobs')
            
        return render(request,'job_detail.html',context)

    def post(self ,request,id):
        if request.method == 'POST':
            letter = request.POST.get('letter')
            try:
                applicant_obj = User.objects.get(username=request.user) 
                driver_obj = Driver.objects.get(user = applicant_obj)
                job_obj = Job.objects.get(id=id)

                application_exist = Application.objects.filter(job = job_obj, driver=driver_obj).first()
                if application_exist:
                    messages.error(request,'Application exists')
                    return redirect(f'/job/{id}')

                new_application = Application(job=job_obj,driver=driver_obj,motivation_letter=letter)
                new_application.save()
                job_obj.applicants = job_obj.applicants + 1
                job_obj.save()
            except Exception as e:
                messages.error(request,e)
                return redirect(f'/job/{id}')

        return redirect(f'/job/{id}')


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
                next_url = request.POST.get('next', request.GET.get('next', '/'))
                netloc = urlparse(next_url).netloc
                if netloc: 
                    next_url = '/'  
                return redirect(next_url)
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