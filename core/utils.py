import os
import pdfrw
from django.core.validators import RegexValidator
from django import forms
from django import template

register = template.Library()

@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__


INVOICE_TEMPLATE_PATH = 'invoice_template.pdf'
INVOICE_OUTPUT_PATH = 'invoice.pdf'


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        print(key, data_dict[key])
                        if data_dict[key] == 'Yes' or data_dict[key] == 'No' or data_dict[key] == 'Off':
                            annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName(data_dict[key])))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
 
def signaturemerger(path, signature, output):
    base_pdf = pdfrw.PdfReader(path)
    signature_pdf = pdfrw.PdfReader(signature)
    mark = signature_pdf.pages[0]
    
    merger = pdfrw.PageMerge(base_pdf.pages[2])
    merger.add(mark).render()
 
    writer = pdfrw.PdfWriter()
    writer.write(output, base_pdf)

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

# def base_create_view(request, **kwargs):
#     if request.method == 'POST':
#         for key, value in kwargs.items():
#             if key != 'form' and key != 'model'
#                 reques.POST[key] = value
#             elif key == 'form':
#                 objForm = value
#             elif key == 'model':
#                 objModel = value
#         try:
#             employee = get_object_or_404(objModel, ssn=request.POST['ssn'])
#             form = EmployeeModelForm(request.POST, instance=employee)
#         except Http404:
#             form = EmployeeModelForm(request.POST)
#         if form.is_valid():
#             saved_data = form.save()
#             # print(saved_data)
#             return redirect(''.join(['/coverage/?employee=', str(saved_data.id)]))
#     print(request.GET.get('id', None))
#     if request.GET.get('id', None):
#         employee = get_object_or_404(EmployeeModel, id=request.GET.get('id', None))
#         print(employee)
#         form = EmployeeModelForm(instance=employee)
#     else:
#         form = EmployeeModelForm(initial={ 'login_user': request.user, 'all_forms_completed': False, 'employer': request.GET.get('employer', None)})
#     return render(request,'healthquestionaire/employee_form.html',{'form': form, 'back_url': '/employer/create/?id=%s' %(request.GET.get('employer', None) if request.GET.get('employer', None) else employee.employer.id)})


class CombinedFormBase(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        # is_valid will trigger clean method
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid() :
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data
