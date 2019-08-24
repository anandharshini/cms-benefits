from django.shortcuts import render
from form_application.models import ApplicationModel
from core.filters import ApplicationModelFilter

# Create your views here.

def broker_home_view(request):
    completed_apps = ApplicationModel.objects.filter(completed=True)
    apps_filter = ApplicationModelFilter(request.GET, queryset=completed_apps)
    return render(request, 'broker_app/broker_home.html', {'filter': apps_filter})
