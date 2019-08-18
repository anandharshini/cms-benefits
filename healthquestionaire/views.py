import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployerAddressForm, EmployeeAddressForm, CoverageForm, EmployeeModelForm
from core.utils import write_fillable_pdf
from .process_submitted_data import process_data
from .forms import MedicalModelFormset, MedicationModelFormset, DependentInfoForm
from .models import MedicalModel, MedicationModel, EmployeeModel, CoverageModel, DependentInfoModel
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404
from form_application.models import ApplicationModel
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import connection
from employer.models import Employer
import pdfrw
import enum


def get_employee_instance(user, employee_id):
    try:
        print(enum.__file__, 'enum')
        if employee_id:
            employee = get_object_or_404(EmployeeModel, id=employee_id)
        elif user:
            employee = get_object_or_404(EmployeeModel, login_user=user)
        else:
            return None
        
        print('employee check', employee_id, employee.id)
        return employee
    except Http404:
        return None
        
def create_medical_model_form(request):
    template_name = 'medical_formset.html'
    heading_message = 'Health Information Details'
    heading_direction = 'If you answer “Yes” to any of the previous Health History questions, please provide detail in form provided below.'
    employee = get_employee_instance(request.user, request.GET.get('employee', None))
    
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = MedicalModelFormset(queryset=MedicalModel.objects.none())
    elif request.method == 'POST':
        formset = MedicalModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # only save if name is present
                if employee:
                    saved_data = form.save(commit=False)
                    saved_data.employee = employee
                    saved_data.save()
            return redirect(''.join([settings.PREFIX_URL, 'medicals/?toolbar_off&employee=', str(employee.id)]))
    return render(request, template_name, {
            'formset': formset,
            'back_url': ''.join([settings.PREFIX_URL,'dependentinfo/?toolbar_off&employee=', str(request.GET.get('employee', ''))]),
            'medical_list': MedicalModel.objects.filter(employee=employee),
            'heading': heading_message,
            'heading_direction': heading_direction,
            'PREFIX_URL': settings.PREFIX_URL,
        })

def create_medication_model_form(request):
    template_name = 'medication_formset.html'
    heading_message = 'Medication List'
    heading_direction = 'Please list any medications, prescriptions, or injections taken in the last 12 months'
    employee = get_employee_instance(request.user, request.GET.get('employee', None))
    
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = MedicationModelFormset(queryset=MedicationModel.objects.none())
    elif request.method == 'POST':
        formset = MedicationModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # only save if name is present
               if employee:
                    saved_data = form.save(commit=False)
                    saved_data.employee = employee
                    saved_data.save()
            return redirect(''.join([settings.PREFIX_URL, 'medications/?toolbar_off&employee=', str(employee.id)]))
    return render(request, template_name, {
            'formset': formset,
            'back_url': ''.join([settings.PREFIX_URL,'dependents/?toolbar_off&employee=', str(request.GET.get('employee', ''))]),
            'medical_list': MedicationModel.objects.filter(employee=employee),
            'heading': heading_message,
            'heading_direction': heading_direction,
            'PREFIX_URL': settings.PREFIX_URL,
        })

def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, as_attachment=True, filename='media/pdf-templates/LHP_Employee_Health_Application_2019.pdf')

# class HealthQuestionView(SessionWizardView):
#     FORMS = [
#         ("employer", EmployerAddressForm),
#         ("employee", EmployeeAddressForm)
#         #  ("coverage", CoverageForm),
#         #  ("dependents", EmployeeDependentForm )
#         ]

#     # TEMPLATES = {"employee": "questions/employee_form.html",
#     #          "coverage": "questions/employee_coverage_form.html",
#     #          "dependents": "questions/employee_dependent_form.html"}
#     template_name = 'health_wizard.html'
#     # def get_template_names(self):
#     #     return [self.TEMPLATES[self.steps.current]]
    
#     def done(self, form_list, **kwargs):
#         submitted_data = [form.cleaned_data for form in form_list]
#         try:
#             employee = process_data(self.request, submitted_data)
#         except Exception as ex:
#             print(ex, 'error generic')
        
#         response = redirect(''.join([settings.PREFIX_URL,'coverage/?toolbar_off&empl_id=', str(employee.id)]))
#         return response


class CoverageModelCreateView(CreateView):
    form_class = CoverageForm
    template_name = "healthquestionaire/coverage_form.html"
    success_url = '/medicals/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = ''.join(['employee/edit/', str(self.request.GET.get('employee', '')), '/?toolbar_off'])
        return context
    
def employeeview(request):
    employer_id = request.GET.get('employer', None)
    heading_message = 'Employee Information'
    heading_direction = 'Please complete all details below.'
    user = request.user
    if request.method == 'POST':
        try:
            # print(request.GET.get('id', None))
            employee = get_object_or_404(EmployeeModel, login_user_id=request.user)
            form = EmployeeModelForm(request.POST, instance=employee)
        except Http404:
            form = EmployeeModelForm(request.POST)
        if form.is_valid():
            saved_data = form.save(commit=False)
            saved_data.login_user = user
            saved_data.all_forms_completed = False
            saved_data.save()
            print(user, 'login user', saved_data.login_user)
            try:
                employer = get_object_or_404(Employer, id=employer_id)
                employer.employee.add(EmployeeModel.objects.get(id=saved_data.id))
            except Http404:
                print('Cannot find employer')            
            return redirect(''.join([settings.PREFIX_URL,'coverage/?toolbar_off&employee=', str(saved_data.id)]))
    print(request.GET.get('id', None))
    if request.GET.get('id', None):
        employee = get_object_or_404(EmployeeModel, id=request.GET.get('id', None))
        print(employee)
        form = EmployeeModelForm(instance=employee)
    else:
        try:
            employee = get_object_or_404(EmployeeModel, login_user=user)
            form = EmployeeModelForm(instance=employee)
        except Http404:
            form = EmployeeModelForm(initial={ 'login_user': request.user, 'all_forms_completed': False})
    return render(request,'healthquestionaire/employee_form.html',{'form': form, 'heading': heading_message, 'heading_direction': heading_direction, 'back_url': settings.PREFIX_URL})

def coverageview(request):
    employee = get_employee_instance(request.user, request.GET.get('employee', None))
    heading_message = 'Insurance Coverage'
    heading_direction = 'Please complete aplicable fields below.'
    if request.method == 'POST':
        print('POST FORM coverage', request.POST)
        try:
            coverage = get_object_or_404(CoverageModel, employee=employee)
            form = CoverageForm(request.POST, instance=coverage)
        except Http404:
            form = CoverageForm(request.POST)
        if form.is_valid():
            if employee:
                saved_data = form.save(commit=False)
                saved_data.employee = employee
                saved_data.save()
            # print(saved_data)
            return redirect(''.join([settings.PREFIX_URL, 'dependents/?toolbar_off&employee=', str(employee.id)]))
        else:
            print(form.errors)

    print(request.GET.get('employee', None))
    if request.GET.get('employee', None):
        print('testing')
        try:
            coverage = get_object_or_404(CoverageModel, employee=employee)
            form = CoverageForm(instance=coverage)
        except Http404:
            form = CoverageForm(initial={'employee': employee})
    else:
        return redirect(''.join([settings.PREFIX_URL, 'employee/create/?toolbar_off']))
    return render(request,'healthquestionaire/coverage_form.html',{'form': form, 'heading': heading_message, 'heading_direction': heading_direction, 'back_url': '%semployee/create/?toolbar_off&id=%s' %(settings.PREFIX_URL, employee.id if employee else coverage.employee.id)})

def dependentinfoview(request):
    print(request.GET.get('employee', None))
    employee = get_employee_instance(request.user, request.GET.get('employee', None))
    heading_message = 'Health Information'
    heading_direction = 'Please provide height and weight for you and your spouse and answer the following health questions regarding any medical conditions or medical treatment for you and your family.'
    if request.method == 'POST':
        try:
            dependentinfo = get_object_or_404(DependentInfoModel, employee=employee)
            form = DependentInfoForm(request.POST, instance=dependentinfo)
        except Http404:
            form = DependentInfoForm(request.POST)
        if form.is_valid():
            if employee:
                saved_data = form.save(commit=False)
                saved_data.employee = employee
                saved_data.save()
            # print(saved_data)
            # app_model = ApplicationModel(
            #     name = employee.form_type, 
            #     submit_user = request.user, 
            #     employee = employee 
            # )
            # try:
            #     app_model.full_clean()
            #     app_model.save()
            # except ValidationError as e:
            #         print(e, 'app model error')
            
            return redirect(''.join([settings.PREFIX_URL, 'medicals/?toolbar_off&employee=', str(employee.id)]))
    if employee:
        try:
            dependent_info = get_object_or_404(DependentInfoModel, employee=employee)
            print(employee)
            form = DependentInfoForm(instance=dependent_info)
        except Http404:
            form = DependentInfoForm(initial={'employee': employee})
    else:
        form = DependentInfoForm()
    back_url = '%smedications/?toolbar_off&employee=%s' %(settings.PREFIX_URL, str(employee.id))
    print(employee.id, back_url)
    return render(request,'healthquestionaire/dependentinfo_form.html',
        {
            'form': form, 
            'heading': heading_message, 
            'heading_direction': heading_direction, 
            'back_url': back_url,
        })

        # 'next_url': '%smedicals/?toolbar_off&employee=%s' %(settings.PREFIX_URL, employee.id)
