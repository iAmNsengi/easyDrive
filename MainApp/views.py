from django.shortcuts import render,redirect
from django.views import View

# Create your views here.
class HomePage(View):
    def get(self,request):
        return render(request,'index.html')