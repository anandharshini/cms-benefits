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
            'back_url': ''.join(['/coverage/?employee=', request.GET.get('employee', None)]),
            'medical_list': MedicalModel.objects.all(),
            'heading': heading_message,
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
        
        response = redirect(''.join(['/coverage/?empl_id=', str(employee.id)]))
        return response


class CoverageModelCreateView(CreateView):
    form_class = CoverageForm
    template_name = "healthquestionaire/coverage_form.html"
    success_url = '/medicals/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = ''.join(['/employee/edit/', self.request.GET.get('employee', None), '/'])
        return context
    
def employeeview(request):
    if request.method == 'POST':
        try:
            print(request.GET.get('id', None))
            employee = get_object_or_404(EmployeeModel, empl_ssn=request.POST['empl_ssn'])
            form = EmployeeModelForm(request.POST, instance=employee)
        except Http404:
            form = EmployeeModelForm(request.POST)
        if form.is_valid():
            form.initial['all_forms_completed'] = False
            form.initial['login_user'] = request.user
            form.initial['employer'] = request.GET.get('employer', None)
            saved_data = form.save()
            # print(saved_data)
            return redirect(''.join(['/coverage/?employee=', str(saved_data.id)]))
    print(request.GET.get('id', None))
    if request.GET.get('id', None):
        employee = get_object_or_404(EmployeeModel, id=request.GET.get('id', None))
        print(employee)
        form = EmployeeModelForm(instance=employee)
    else:
        form = EmployeeModelForm(initial={ 'login_user': request.user, 'all_forms_completed': False, 'employer': request.GET.get('employer', None)})
    return render(request,'healthquestionaire/employee_form.html',{'form': form, 'back_url': '/employer/create/?id=%s' %(request.GET.get('employer', None) if request.GET.get('employer', None) else (str(employee.employer.id) if employee.employer else ''))})

def coverageview(request):
    if request.method == 'POST':
        print('POST FORM coverage', request.POST)
        try:
            coverage = get_object_or_404(CoverageModel, employee=request.GET.get('employee', None))
            form = CoverageForm(request.POST, instance=coverage)
        except Http404:
            form = CoverageForm(request.POST)
        if form.is_valid():
            saved_data = form.save()
            print(saved_data)
            return redirect(''.join(['/medicals/?employee=', request.GET.get('employee', None)]))
        else:
            print(form.errors)

    print(request.GET.get('employee', None))
    if request.GET.get('employee', None):
        print('testing')
        try:
            coverage = get_object_or_404(CoverageModel, employee=request.GET.get('employee', None))
            form = CoverageForm(instance=coverage)
        except Http404:
            form = CoverageForm(initial={'employee': request.GET.get('employee', None)})
    else:
        form = CoverageForm()
    return render(request,'healthquestionaire/coverage_form.html',{'form': form, 'back_url': '/employee/create/?id=%s' %(request.GET.get('employee', None) if request.GET.get('employee', None) else coverage.employee.id)})

def dependentinfoview(request):
    if request.method == 'POST':
        try:
            employee = get_object_or_404(DependentInfoModel, employee=request.GET.get('employee', None))
            form = DependentInfoForm(request.POST, instance=employee)
        except Http404:
            form = DependentInfoForm(request.POST)
        if form.is_valid():
            saved_data = form.save()
            # print(saved_data)
            return redirect(''.join(['/coverage/?employee=', str(saved_data.id)]))
    if request.GET.get('employee', None):
        try:
            employee = get_object_or_404(DependentInfoModel, employee=request.GET.get('employee', None))
            print(employee)
            form = DependentInfoForm(instance=employee)
        except Http404:
            form = DependentInfoForm(initial={'employee': request.GET.get('employee', None)})
    else:
        form = DependentInfoForm(initial={ 'employee': request.GET.get('employee', None)})
    return render(request,'healthquestionaire/dependentinfo_form.html',{'form': form, 'back_url': '/medications/employee=%s' %(request.GET.get('employee', None))})
