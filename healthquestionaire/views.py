import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from formtools.wizard.views import SessionWizardView
from django.shortcuts import render
from .forms import EmployeeForm, CoverageForm
from core.forms import EmployeeDependentForm
from core.utils import write_fillable_pdf

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
    FORMS = [("employee", EmployeeForm),
         ("coverage", CoverageForm),
         ("dependents", EmployeeDependentForm )]

    TEMPLATES = {"employee": "questions/employee_form.html",
             "coverage": "questions/employee_coverage_form.html",
             "dependents": "questions/employee_dependent_form.html"}
    template_name = 'health_wizard.html'
    # def get_template_names(self):
    #     return [self.TEMPLATES[self.steps.current]]
    
    def done(self, form_list, **kwargs):
        submitted_data = [form.cleaned_data for form in form_list]
        print(submitted_data)
        try:
            write_fillable_pdf('media/pdf-templates/LHP_Employee_Health_Application_2019.pdf', 'media/submitted/%s_submitted.pdf' %(self.request.user.id), submitted_data[0])
        except Exception as ex:
            print(ex)
        return render(self.request, 'done.html', {
            'form_data': [],
        })
