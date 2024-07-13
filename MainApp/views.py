from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout,authenticate
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
class HomePage(View):
    def get(self,request):
        return render(request,'index.html')


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