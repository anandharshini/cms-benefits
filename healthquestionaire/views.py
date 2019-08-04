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

def get_employee_instance(user, employee_id):
    try:
        if employee_id:
            employee = get_object_or_404(EmployeeModel, id=employee_id)
        elif user:
            employee = get_object_or_404(EmployeeModel, login_user=user)
        else:
            return redirect(''.join([settings.PREFIX_URL, 'employee/create/?toolbar_off']))
        return employee
    except Http404:
        return redirect(''.join([settings.PREFIX_URL, 'employee/create/?toolbar_off']))
        
def create_medical_model_form(request):
    template_name = 'medical_formset.html'
    heading_message = 'Medical Form'
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
            'back_url': ''.join([settings.PREFIX_URL,'dependents/?toolbar_off&employee=', str(request.GET.get('employee', ''))]),
            'medical_list': MedicalModel.objects.filter(employee=employee),
            'heading': heading_message,
            'PREFIX_URL': settings.PREFIX_URL,
        })

def create_medication_model_form(request):
    template_name = 'medication_formset.html'
    heading_message = 'Medication Form'
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
            'back_url': ''.join([settings.PREFIX_URL,'medical/?toolbar_off&employee=', str(request.GET.get('employee', ''))]),
            'medical_list': MedicationModel.objects.filter(employee=employee),
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
    user = request.user
    if request.method == 'POST':
        try:
            print(request.GET.get('id', None))
            employee = get_object_or_404(EmployeeModel, empl_ssn=request.POST['empl_ssn'])
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
    return render(request,'healthquestionaire/employee_form.html',{'form': form, 'back_url': settings.PREFIX_URL})

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
            # print(saved_data)
            return redirect(''.join([settings.PREFIX_URL, 'dependents/?toolbar_off&employee=', employee_id]))
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
        return redirect(''.join([settings.PREFIX_URL, 'employee/create/?toolbar_off']))
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
            pdf_data = {}
            with connection.cursor() as cursor:
                sql = """
                    select emplr.name as section_1_employer_name, emplr.street as section_1_street_address, emplr.city as section_1_city, emplr.state as section_1_state, emplr.zip_code as section_1_zip,
                    empls.empl_first_name || ' ' || empls.empl_last_name as section_2_employee_full_name, empls.empl_hire_date assection_2_hire_date, empls.empl_dob as section_2_employee_birth_date,
                    empls.street as section_2_street_address, empls.city as section_2_city, empls.state as section_2_state, empls.zip_code as section_2_zip,
                    empls.empl_ssn as section_2_employee_ssn, empls.empl_gender_id as section_2_gender, case when hcm.tobacco_use_id = 18 then 'Yes' else 'No' end as section_2_tobacco_use_yes, case when hcm.tobacco_use_id = 19 then 'Yes' else 'No' end as section_2_tobacco_use_no,
                    case when empls.marital_status_id = 26 then 'Yes' else 'No' end as section_2_marital_status_married ,
                    case when empls.marital_status_id = 27 then 'Yes' else 'No' end as section_2_marital_status_single,
                    case when empls.marital_status_id = 28 then 'Yes' else 'No' end as section_2_marital_status_widowed,
                    case when empls.marital_status_id = 29 then 'Yes' else 'No' end as section_2_marital_status_divorced,
                    empls.home_phone as section_2_home_phone, empls.cell_phone as section_2_cell_phone, empls.email_address as section_2_email_address,
                    empls.job_title as section_2_job_title, empls.hours_worked_per_week as section_2_hours_worked_per_week, empls.spouse_employer as section_2_spouse_employer, empls.spouse_buisness_phone as section_2_spouse_business_phone,
                    case when hcm.dependent_disabled_id = 18 then 'Yes' else 'Off' end as section_3_dependents_disabled_yes,
                    case when hcm.dependent_disabled_id = 19 then 'Yes' else 'Off' end as section_3_dependents_disabled_no, hcm.dependent_disabled_name as section_3_dependents_disabled_names,
                    case when hcm.dependent_insurance_other_continue_id = 18 then 'Yes' else 'Off' end as section_3_insurance_other_yes,
                    case when hcm.dependent_insurance_other_continue_id = 19 then 'Yes' else 'Off' end as section_3_insurance_other_no, hcm.dependent_isu_coverage_carrier as section_3_name_of_other_health_insurance_carrier,
                    hcm.effective_date as section_3_effective_date, 
                    case when hcm.coverage_id = 20 then 'Yes' else 'Off' end as section_5_elect_coverage,
                    case when hcm.coverage_id = 21 then 'Yes' else 'Off' end as section_5_decline_coverage,
                    case when hcmcl.lookupmodel_id = 22 then 'Yes' else 'No' end as section_5_employee_only,
                    case when hcmcl.lookupmodel_id = 23 then 'Yes' else 'No' end as section_5_employee_spouse ,
                    case when hcmcl.lookupmodel_id = 24 then 'Yes' else 'No' end as section_5_employee_children ,
                    case when hcmcl.lookupmodel_id = 25 then 'Yes' else 'No' end as section_5_family,
                    case when hcmdr.lookupmodel_id = 30 then 'Yes' else 'No' end as section_5_spouse_employer_plan,
                    case when hcmdr.lookupmodel_id = 31 then 'Yes' else 'No' end as section_5_individual_plan ,
                    case when hcmdr.lookupmodel_id = 32 then 'Yes' else 'No' end as section_5_medicare ,
                    case when hcmdr.lookupmodel_id = 33 then 'Yes' else 'No' end as section_5_medicaid,
                    case when hcmdr.lookupmodel_id = 34 then 'Yes' else 'No' end as section_5_cobra_from_previous_employer,
                    case when hcmdr.lookupmodel_id = 35 then 'Yes' else 'No' end as section_5_va_eligibility,
                    case when hcmdr.lookupmodel_id = 36 then 'Yes' else 'No' end as section_5_no_other_coverage_at_this_time,
                    case when hcmdr.lookupmodel_id = 37 then 'Yes' else 'No' end as section_5_other,
                    hcm.others as section_5_reason_for_decline
                    
                    from employers_employee emplr_emply 
                    inner join employers emplr on emplr.id = emplr_emply.employer_id
                    inner join employees empls on empls.id = emplr_emply.employeemodel_id
                    inner join healthquestionaire_coveragemodel hcm on hcm.employee_id = empls.id 
                    inner join healthquestionaire_coveragemodel_coverage_level hcmcl on hcmcl.coveragemodel_id = hcm.id
                    left outer join healthquestionaire_coveragemodel_decline_reasons hcmdr on hcmdr.coveragemodel_id = hcm.id
                    where emplr_emply.employeemodel_id = """ + str(employee_id) + """ order by hcm.effective_date desc limit 1 """
                try:
                    cursor.execute(sql)
                    columns = [col[0] for col in cursor.description]
                    data = [dict(zip(columns, row))
                        for row in cursor.fetchall()]
                    # print(data[0])
                    pdf_data = data[0]
                    # sql = """
                    #     select case when value_1 is not null then 'Yes' else 'No' end as section_6_cardiac_disorder_yes,
                    #         case when value_1 is null then 'Yes' else 'No' end as section_6_cardiac_disorder_no,
                    #         case when value_2 is not null then 'Yes' else 'No' end as section_6_cancer_tumor_yes,
                    #         case when value_2 is null then 'Yes' else 'No' end as section_6_cancer_tumor_no,
                    #         case when value_3 is not null then 'Yes' else 'No' end as section_6_diabetes_yes,
                    #         case when value_3 is null then 'Yes' else 'No' end as section_6_diabetes_no,
                    #         case when value_4 is not null then 'Yes' else 'No' end as section_6_kidney_disorder_yes,
                    #         case when value_4 is null then 'Yes' else 'No' end as section_6_kidney_disorder_no,
                    #         case when value_5 is not null then 'Yes' else 'No' end as section_6_respiratory_disorder_yes,
                    #         case when value_5 is null then 'Yes' else 'No' end as section_6_respiratory_disorder_no,
                    #         case when value_6 is not null then 'Yes' else 'No' end as section_6_liver_disorder_yes,
                    #         case when value_6 is null then 'Yes' else 'No' end as section_6_liver_disorder_no,
                    #         case when value_7 is not null then 'Yes' else 'No' end as section_6_high_blood_pressure_yes,
                    #         case when value_7 is null then 'Yes' else 'No' end as section_6_high_blood_pressure_no,
                    #         case when value_8 is not null then 'Yes' else 'No' end as section_6_aids_hiv_immune_system_disorder_yes,
                    #         case when value_8 is null then 'Yes' else 'No' end as section_6_aids_hiv_immune_system_disorder_no,
                    #         case when value_9 is not null then 'Yes' else 'No' end as section_6_alcohol_drug_abuse_yes,
                    #         case when value_9 is null then 'Yes' else 'No' end as section_6_alcohol_drug_abuse_no,
                    #         case when value_10 is not null then 'Yes' else 'No' end as section_6_mental_nervous_disorder_yes,
                    #         case when value_10 is null then 'Yes' else 'No' end as section_6_mental_nervous_disorder_no,
                    #         case when value_11 is not null then 'Yes' else 'No' end as section_6_neuro_muscular_yes,
                    #         case when value_11 is null then 'Yes' else 'No' end as section_6_neuro_muscular_no,
                    #         case when value_12 is not null then 'Yes' else 'No' end as section_6_stomach_gastrointestinal_yes,
                    #         case when value_12 is null then 'Yes' else 'No' end as section_6_stomach_gastrointestinal_no,
                    #         case when value_13 is not null then 'Yes' else 'No' end as section_6_joint_disorder_yes,
                    #         case when value_13 is null then 'Yes' else 'No' end as section_6_joint_disorder_no,
                    #         case when value_14 is not null then 'Yes' else 'No' end as section_6_seizures_convulsion_epilepsy_yes,
                    #         case when value_14 is null then 'Yes' else 'No' end as section_6_seizures_convulsion_epilepsy_no,
                    #         case when value_15 is not null then 'Yes' else 'No' end as section_6_any_other_medical_condition_yes,
                    #         case when value_15 is null then 'Yes' else 'No' end as section_6_any_other_medical_condition_no


                    #     from crosstab($$ select hdi.employee_id as id, value_lookup as attr, hdidt.lookupmodel_id = lkup.id as value from lookup_data lkup 
                    #     left join healthquestionaire_dependentinfomodel hdi on hdi.employee_id = """ + str(employee_id) + """
                    #     Left join healthquestionaire_dependentinfomodel_diagnose_treated hdidt on hdidt.dependentinfomodel_id = hdi.id and  hdidt.lookupmodel_id = lkup.id
                    #     where lkup.type_lookup = 'med_conditions' order by 1 $$) as ct (employee_id int, value_1 bool, value_2 bool,value_3 bool, value_4 bool,value_5 bool, value_6 bool,value_7 bool, value_8 bool,value_9 bool, value_10 bool,value_11 bool, value_12 bool, value_13 bool, value_14 bool, value_15 bool)
                    # """
                    # cursor.execute(sql)
                    # columns = [col[0] for col in cursor.description]
                    # data_med_conditions = [dict(zip(columns, row))
                    #     for row in cursor.fetchall()]
                    # if data_med_conditions:
                    #     for (key, value) in data_med_conditions[0].items():
                    #     # Check if key is even then add pair to new dictionary
                    #         # if value == 'Yes':
                    #         #     data_med_conditions[0][key] = pdfrw.PdfName('Yes')
                            
                    #         pdf_data[key] = value
                    # print(pdf_data)
                    sql = """
                        select case when hdi.past_5_insu_decl_id = 18 then 'Yes' else 'No' end as section_6_question_2_yes,
                        case when hdi.past_5_insu_decl_id = 19 then 'Yes' else 'No' end as section_6_question_2_no,
                        case when hdi.past_24_med_cond_id = 18 then 'Yes' else 'No' end as section_6_question_3_yes,
                        case when hdi.past_24_med_cond_id = 19 then 'Yes' else 'No' end as section_6_question_3_no,
                        case when hdi.past_24_mon_med_exp_5k_id = 18 then 'Yes' else 'No' end as section_6_question_4_yes,
                        case when hdi.past_24_mon_med_exp_5k_id = 19 then 'Yes' else 'No' end as section_6_question_4_no,
                        case when hdi.anticipate_hozpital_id = 18 then 'Yes' else 'No' end as section_6_question_5_yes,
                        case when hdi.anticipate_hozpital_id = 19 then 'Yes' else 'No' end as section_6_question_5_no,
                        case when hdi.dependent_pregnant_id = 18 then 'Yes' else 'No' end as section_6_question_6_yes,
                        case when hdi.dependent_pregnant_id = 19 then 'Yes' else 'No' end as section_6_question_6_no
                        from healthquestionaire_dependentinfomodel hdi where hdi.employee_id = """ + str(employee_id)
                    cursor.execute(sql)
                    columns = [col[0] for col in cursor.description]
                    data_med_info = [dict(zip(columns, row))
                        for row in cursor.fetchall()]
                    if data_med_info:
                        for (key, value) in data_med_info[0].items():
                            pdf_data[key] = value
                    # Adding Employee Dependents to pdf form
                    sql = """
                    select empldep.first_name || ' ' || empldep.last_name as section_4_first_name_last_name_row, (select value_lookup from lookup_data where id = empldep.relationship_id limit 1) as section_4_relationship_row,
                        empldep.ssn as section_4_ssn_row, empldep.dob_dependent as section_4_doc_row, empldep.age as section_4_age_row, (select value_lookup from lookup_data where id = empldep.gender_id limit 1) as section_4_gender_row
                        from employee_dependents empldep where employee_id = """ + str(employee_id)
                    cursor.execute(sql)
                    columns = [col[0] for col in cursor.description]
                    data_med_info = [dict(zip(columns, row))
                        for row in cursor.fetchall()]
                    if data_med_info:
                        for (key, value, index) in data_med_info[0].items():
                            pdf_data[''.join([key,'_', index])] = value
                    # Adding medical conditions to pdf form
                    sql = """
                    select hmedcond.family_member as section_6_question_7_family_member_row, hmedcond.disease_diag_treat as section_6_question_7_disease_row, hmedcond.date_of_onset as section_6_question_7_date_of_onset_row, 
                        hmedcond.date_last_seen as section_6_question_7_date_last_seen_row, hmedcond.remaining_symp_probs as section_6_question_7_remaining_symptoms_row
                        from healthquestionaire_medicalmodel hmedcond where employee_id = """ + str(employee_id)
                    cursor.execute(sql)
                    columns = [col[0] for col in cursor.description]
                    data_med_info = [dict(zip(columns, row))
                        for row in cursor.fetchall()]
                    if data_med_info:
                        for (key, value, index) in data_med_info[0].items():
                            pdf_data[''.join([key,'_', index])] = value
                    
                    # Adding prescriptions to PDF form
                    sql = """
                    select hmedm.family_member as section_6_question_8_family_member_name_row, hmedm.medication_rx_injection as section_6_question_8_medication_row, hmedm.dosage as section_6_question_8_dosage_row, 
                        hmedm.med_condition as section_6_question_8_medical_condition_row
                        from healthquestionaire_medicationmodel hmedm where employee_id = """ + str(employee_id)
                    cursor.execute(sql)
                    columns = [col[0] for col in cursor.description]
                    data_med_info = [dict(zip(columns, row))
                        for row in cursor.fetchall()]
                    if data_med_info:
                        for (key, value, index) in data_med_info[0].items():
                            pdf_data[''.join([key,'_', index])] = value

                    write_fillable_pdf('media/pdf-templates/LHP_Employee_Health_Application_2019(120618)(Fillable).pdf', ''.join(['media/submitted/', str(employee_id), '.pdf']), pdf_data)
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
