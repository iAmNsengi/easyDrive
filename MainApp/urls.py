from django.urls import path
from .views import *

urlpatterns =[
    path('',HomePage.as_view()),
    path('jobs/',Jobs.as_view()),
    path('add_job/',AddJob.as_view()),
    path('job/<str:id>',JobDetail.as_view()),
    path('profile/',DriverProfile.as_view()),

    path('login/',Login.as_view()),
    path('register/',Register.as_view()),
    path('logout/',Logout)

]