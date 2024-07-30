from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date



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
                messages.success(request,"Application sent successfully!")
            except Exception as e:
                messages.error(request,e)
                return redirect(f'/job/{id}')

        return redirect(f'/job/{id}')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        context ={}
        user = request.user
        driver_profile = Driver.objects.filter(user=user).first()
        company_profile = Company.objects.filter(user=user).first()
        
        if driver_profile:
            # Jobs applied to by this driver
            applications = Application.objects.filter(driver=driver_profile)
            context = {
                'driver_profile': driver_profile,
                'applications': applications,
            }
        elif company_profile:
            # Jobs created by this company
            jobs_created = Job.objects.filter(creator=user)
            context = {
                'company_profile': company_profile,
                'jobs_created': jobs_created,
            }
        
        return render(request, 'profile.html', context)

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        if Driver.objects.filter(user=user).exists():
            try:

                driver_profile = Driver.objects.get(user=user)
                driver_profile.avatar = request.FILES.get('avatar', driver_profile.avatar)
                driver_profile.category = request.POST.get('category')
                driver_profile.bio = request.POST.get('bio')
                driver_profile.status = request.POST.get('status')
                driver_profile.experience = request.POST.get('experience_years') or 0
                driver_profile.license_number = request.POST.get('license_number')
                driver_profile.license_type = request.POST.get('license_type')
                driver_profile.license_expiration = request.POST.get('license_expiration') or None
                driver_profile.salary = request.POST.get('salary') or 0
                driver_profile.rating = request.POST.get('rating') or 0
                driver_profile.save()
                messages.success(request,'Updated successfully')
            except Exception as e:
                messages.error(request,e)
                return redirect('/profile')
        else:
            try:
                company_profile = Company.objects.get(user=user)
                company_profile.avatar = request.FILES.get('avatar', company_profile.avatar)
                company_profile.name = request.POST.get('name')
                company_profile.location = request.POST.get('location')
                company_profile.bio = request.POST.get('bio')
                company_profile.contact_email = request.POST.get('contact_email')
                company_profile.contact_phone = request.POST.get('contact_phone')
                company_profile.save()
                messages.success(request,'Updated successfully')
            except Exception as e:
                messages.error(request,e)
                return redirect('/profile')

        return redirect('/profile')

def update_job_status(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        job.status = new_status
        job.save()
        return redirect('/profile') 

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