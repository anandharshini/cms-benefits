from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployerForm
from .models import Employer
from django.http import Http404
from django.conf import settings
from form_application.models import ApplicationModel
from core.filters import ApplicationModelFilter
from healthquestionaire.views import get_employee_instance
# from django.views.generic import ListView, DetailView
# #home view for employers. employers are displayed in a list
# class IndexView(ListView):
#     template_name='index.html'
#     context_object_name = 'employer_list'
#     def get_queryset(self):
#         return Employer.objects.all()
# #Detail view (view employer detail)
# class EmployerDetailView(DetailView):
#     model=Employer
#     template_name = 'employer-detail.html'
#New Employer view (Create new Employer)

def show_employees_apps(request):
    employee = get_employee_instance(request.user, request.GET.get('employee', None))
    employee_apps = ApplicationModel.objects.filter(employee__fk_employer=employee.fk_employer)
    apps_filter = ApplicationModelFilter(request.GET, queryset=employee_apps)
    return render(request, 'employer/employee_apps.html', {'filter': apps_filter, 'download_url': settings.DOWNLOAD_URL})


def employerview(request):
    if request.method == 'POST':
        try:
            employer = get_object_or_404(Employer, name=request.POST['name'])
            form = EmployerForm(request.POST, instance=employer)
        except Http404:
            form = EmployerForm(request.POST)
        if form.is_valid():
            saved_data = form.save()
            print(saved_data)
            return redirect(''.join([settings.PREFIX_URL,'employee/create/?toolbar_off&employer=', str(saved_data.id)]))
    print(request.GET.get('id', None))
    if request.GET.get('id', None):
        employer = get_object_or_404(Employer, id=request.GET.get('id', None))
        print(employer)
        form = EmployerForm(instance=employer)
    else:
        form = EmployerForm()
    return render(request,'employer_form.html',{'form': form})
#Edit a employer
def edit(request, pk, template_name='employer_form.html'):
    employer= get_object_or_404(Employer, pk=pk)
    form = EmployerForm(request.POST or None, instance=employer)
    if form.is_valid():
        saved_data = form.save()
        return redirect(''.join([settings.PREFIX_URL, 'employee/?toolbar_off&employer=',saved_data.id]))
    return render(request, template_name, {'form':form})
# #Delete employer
# def delete(request, pk, template_name='confirm_delete.html'):
#     employer= get_object_or_404(Employer, pk=pk)    
#     if request.method=='POST':
#         employer.delete()
#         return redirect('index')
#     return render(request, template_name, {'object':employer})

