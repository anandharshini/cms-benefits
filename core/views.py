from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from core.forms import SignUpForm, EmployeeDependentForm
from core.tokens import account_activation_token
from .models import EmployeeDependent
from django.conf import settings
from healthquestionaire.models import EmployeeModel
from django.http import Http404
from django.conf import settings
from healthquestionaire.views import get_employee_instance

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
            return redirect('/dev/accounts/login/?toolbar_off')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

def create_dependents_model_form(request):
    employee = get_employee_instance(request.user, request.GET.get('employee', None))
    heading_message = 'Dependents'
    if request.method == 'POST':
        print('POST FORM Employee Dependent', request.POST)
        try:
            coverage = get_object_or_404(EmployeeDependent, employee=employee)
            form = EmployeeDependentForm(request.POST, instance=coverage)
        except Http404:
            form = EmployeeDependentForm(request.POST)
        if form.is_valid():
            saved_data = form.save()
            print(saved_data)
            return redirect(''.join([settings.PREFIX_URL,'medicals/?toolbar_off&employee=', str(employee.id)]))
        else:
            print(form.errors)

    print(request.GET.get('employee', None))
    if request.GET.get('employee', None):
        print('testing')
        try:
            coverage = get_object_or_404(EmployeeDependent, employee=employee)
            form = EmployeeDependentForm(instance=coverage)
        except Http404:
            form = EmployeeDependentForm(initial={'employee': employee})
    else:
        return redirect(''.join([settings.PREFIX_URL, 'employee/create/?toolbar_off']))
    return render(request,'dependents_formset.html',
        {
            'form': form, 
            'back_url': ''.join([settings.PREFIX_URL,'coverage/?toolbar_off&employee=', str(request.GET.get('employee', ''))]),
            'next_url': ''.join([settings.PREFIX_URL,'medicals/?toolbar_off&employee=', str(request.GET.get('employee', ''))]),
            'employee_depedents': EmployeeDependent.objects.filter(employee=employee),
            'heading': heading_message,
            'PREFIX_URL': settings.PREFIX_URL,
        })
