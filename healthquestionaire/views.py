import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployerAddressForm, EmployeeAddressForm, CoverageForm, EmployeeDependentForm, EmployeeModelForm
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

def create_medical_model_form(request):
    template_name = 'medical_formset.html'
    heading_message = 'Medical Form'
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = MedicalModelFormset(queryset=MedicalModel.objects.none())
    elif request.method == 'POST':
        formset = MedicalModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # only save if name is present
                if form.cleaned_data.get('family_member'):
                    form.save()
            return redirect('.')
    return render(request, template_name, {
            'formset': formset,
            'back_url': ''.join([settings.PREFIX_URL,'coverage/?toolbar_off&employee=', str(request.GET.get('employee', ''))]),
            'medical_list': MedicalModel.objects.all(),
            'heading': heading_message,
            'PREFIX_URL': settings.PREFIX_URL,
        })

def create_medication_model_form(request):
    template_name = 'medication_formset.html'
    heading_message = 'Medication Form'
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = MedicationModelFormset(queryset=MedicationModel.objects.none())
    elif request.method == 'POST':
        formset = MedicationModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # only save if name is present
                if form.cleaned_data.get('family_member'):
                    form.save()
            return redirect('.')
    return render(request, template_name, {
            'formset': formset,
            'medical_list': MedicationModel.objects.all(),
            'heading': heading_message,
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

class HealthQuestionView(SessionWizardView):
    FORMS = [
        ("employer", EmployerAddressForm),
        ("employee", EmployeeAddressForm)
        #  ("coverage", CoverageForm),
        #  ("dependents", EmployeeDependentForm )
        ]

    # TEMPLATES = {"employee": "questions/employee_form.html",
    #          "coverage": "questions/employee_coverage_form.html",
    #          "dependents": "questions/employee_dependent_form.html"}
    template_name = 'health_wizard.html'
    # def get_template_names(self):
    #     return [self.TEMPLATES[self.steps.current]]
    
    def done(self, form_list, **kwargs):
        submitted_data = [form.cleaned_data for form in form_list]
        try:
            employee = process_data(self.request, submitted_data)
        except Exception as ex:
            print(ex, 'error generic')
        
        response = redirect(''.join([settings.PREFIX_URL,'coverage/?toolbar_off&empl_id=', str(employee.id)]))
        return response


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
    user_id = request.user
    if request.method == 'POST':
        try:
            print(request.GET.get('id', None))
            employee = get_object_or_404(EmployeeModel, empl_ssn=request.POST['empl_ssn'])
            form = EmployeeModelForm(request.POST, instance=employee)
        except Http404:
            form = EmployeeModelForm(request.POST)
        if form.is_valid():
            form.initial['all_forms_completed'] = False
            form.initial['login_user'] = user_id
            saved_data = form.save()
            # print(saved_data)
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
        form = EmployeeModelForm(initial={ 'login_user': request.user.id, 'all_forms_completed': False})
    return render(request,'healthquestionaire/employee_form.html',{'form': form, 'back_url': '%semployer/create/?toolbar_off&id=%s' %(settings.PREFIX_URL, employer_id if employer_id else '')})

def coverageview(request):
    employee_id = request.GET.get('employee', None)
    if request.method == 'POST':
        print('POST FORM coverage', request.POST)
        try:
            coverage = get_object_or_404(CoverageModel, employee=employee_id)
            form = CoverageForm(request.POST, instance=coverage)
        except Http404:
            form = CoverageForm(request.POST)
        if form.is_valid():
            saved_data = form.save()
            print(saved_data)
            return redirect(''.join([settings.PREFIX_URL, 'medicals/?toolbar_off&employee=', employee_id]))
        else:
            print(form.errors)

    print(request.GET.get('employee', None))
    if request.GET.get('employee', None):
        print('testing')
        try:
            coverage = get_object_or_404(CoverageModel, employee=employee_id)
            form = CoverageForm(instance=coverage)
        except Http404:
            form = CoverageForm(initial={'employee': employee_id})
    else:
        form = CoverageForm()
    return render(request,'healthquestionaire/coverage_form.html',{'form': form, 'back_url': '%semployee/create/?toolbar_off&id=%s' %(settings.PREFIX_URL, employee_id if employee_id else coverage.employee.id)})

def dependentinfoview(request):
    employee_id=request.GET.get('employee', None)
    if request.method == 'POST':
        try:
            employee = get_object_or_404(DependentInfoModel, employee=employee_id)
            form = DependentInfoForm(request.POST, instance=employee)
        except Http404:
            form = DependentInfoForm(request.POST)
        if form.is_valid():
            saved_data = form.save()
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
            pdf_data = None
            with connection.cursor() as cursor:
                sql = """
                    select emplr.name as section_1_employer_name, emplr.street as section_1_street_address, emplr.city as section_1_city, emplr.state as section_1_state, emplr.zip_code as section_1_zip,
                    empls.empl_full_name as section_2_employee_full_name, empls.empl_hire_date assection_2_hire_date, empls.empl_dob as section_2_employee_birth_date,
                    empls.street as section_2_street_address, empls.city as section_2_city, empls.state as section_2_state, empls.zip_code as section_2_zip,
                    empls.empl_ssn as section_2_employee_ssn, empls.empl_gender_id as section_2_gender, case when hcm.tobacco_use_id = 18 then 'On' else 'No' end as section_2_tobacco_use_yes, case when hcm.tobacco_use_id = 19 then 'Yes' else 'No' end as section_2_tobacco_use_no,
                    case when empls.marital_status_id = 26 then 'Yes' else 'Off' end as section_2_marital_status_married ,
                    case when empls.marital_status_id = 27 then 'yes' else 'No' end as section_2_marital_status_single,
                    case when empls.marital_status_id = 28 then 'yes' else 'No' end as section_2_marital_status_widowed,
                    case when empls.marital_status_id = 27 then 'yes' else 'No' end as section_2_marital_status_divorced 
                    from employers_employee emplr_emply 
                    inner join employers emplr on emplr.id = emplr_emply.employer_id
                    inner join employees empls on empls.id = emplr_emply.employeemodel_id
                    inner join healthquestionaire_coveragemodel hcm on hcm.employee_id = empls.id where emplr_emply.employeemodel_id = """ + str(employee_id)
                try:
                    cursor.execute(sql)
                    columns = [col[0] for col in cursor.description]
                    data = [dict(zip(columns, row))
                        for row in cursor.fetchall()]
                    print(data)
                    if data:
                        write_fillable_pdf('media/pdf-templates/LHP_Employee_Health_Application_2019(120618)(Fillable).pdf', ''.join(['media/submitted/', str(employee_id), '.pdf']), data[0])
                finally:
                    cursor.close()
            return render(request, 'healthquestionaire/done.html', {
                'PREFIX_URL': settings.PREFIX_URL
            })
    if employee_id:
        try:
            employee = get_object_or_404(DependentInfoModel, employee=employee_id)
            print(employee)
            form = DependentInfoForm(instance=employee)
        except Http404:
            form = DependentInfoForm(initial={'employee': employee_id})
    else:
        form = DependentInfoForm()
    return render(request,'healthquestionaire/dependentinfo_form.html',{'form': form, 'back_url': '%smedications/?toolbar_off&employee=%s' %(settings.PREFIX_URL, employee_id)})
