from django.shortcuts import render

# Create your views here.

def broker_home_view(request):
    return render(request,'broker_app/broker_home.html',{})