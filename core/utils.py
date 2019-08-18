import os
import pdfrw
from django.core.validators import RegexValidator
from django import forms
from django import template
from datetime import date 
from django.db import connection
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

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

def annotate_pdf(template_pdf, data_dict):
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    print(key)
                    if key in data_dict.keys():
                        print(key, data_dict[key])
                        if data_dict[key] == 'Yes' or data_dict[key] == 'No' or data_dict[key] == 'Off':
                            annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName(data_dict[key])))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )

def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    try:
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3_response_object = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key='static/media/pdf-templates/LHP_Employee_Health_Application_2019(120618)(Fillable).pdf')
        object_content = s3_response_object['Body'].read()
        template_pdf = pdfrw.PdfReader(fdata=object_content)
    except Exception as ex:
        print(ex, 'error reading from s3 pdf-templates')
    
    annotate_pdf(template_pdf, data_dict)
                        
    try:
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
    except Exception as ex:
        print(ex, 'error writing to temp folder pdfrw')
  
def calculateAge(birthDate): 
    today = date.today() 
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    return age 

def signaturemerger(path, signature, output, data_dict):
    base_pdf = pdfrw.PdfReader(path)
    signature_pdf = pdfrw.PdfReader(signature)
    mark = signature_pdf.pages[0]
    
    merger = pdfrw.PageMerge(base_pdf.pages[2])
    merger.add(mark).render()

    annotate_pdf(base_pdf, data_dict)
 
    writer = pdfrw.PdfWriter()
    writer.write(output, base_pdf)

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

height_regex = RegexValidator(regex=r'^d{1}\'d{012}\"$', message="Height(X'-XX\")" )
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

def check_signed_file_exists(employee_id):
    # return False
    try:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3_key = ''.join(['static/media/submitted/', str(employee_id), '_signed_pdf.pdf'])
        bucket = settings.AWS_STORAGE_BUCKET_NAME
    
        content = client.head_object(Bucket=bucket,Key=s3_key)
        if content.get('ResponseMetadata',None) is not None:
            return True
        else:
            return False
    except Exception as ex:
        return False

def create_pdf_files(employee_id):
    pdf_data = {}
    with connection.cursor() as cursor:
        sql = """
        select emplr.name as section_1_employer_name, emplr.street as section_1_street_address, emplr.city as section_1_city, emplr.state as section_1_state, emplr.zip_code as section_1_zip,
            empls.empl_first_name || ' ' || empls.empl_last_name as section_2_employee_full_name, empls.empl_hire_date as section_2_hire_date, empls.empl_dob as section_2_employee_birth_date,
            empls.street as section_2_street_address, empls.city as section_2_city, (Select value_lookup from lookup_data where id = empls.state_id limit 1) as section_2_state, empls.zip_code as section_2_zip,
            empls.empl_ssn as section_2_employee_ssn, empls.empl_gender_id as section_2_gender, case when hcm.tobacco_use_id = 18 then 'Yes' else 'No' end as section_2_tobacco_use_yes, case when hcm.tobacco_use_id = 19 then 'Yes' else 'No' end as section_2_tobacco_use_no,
            case when empls.marital_status_id = 26 then 'Yes' else 'No' end as section_2_marital_status_married ,
            case when empls.marital_status_id = 27 then 'Yes' else 'No' end as section_2_marital_status_single,
            case when empls.marital_status_id = 28 then 'Yes' else 'No' end as section_2_marital_status_widowed,
            case when empls.marital_status_id = 29 then 'Yes' else 'No' end as section_2_marital_status_divorced,
            empls.home_phone as section_2_home_phone, empls.cell_phone as section_2_cell_phone, empls.email_address as section_2_email_address,
            empls.job_title as section_2_job_title, (Select value_lookup from lookup_data where id = empls.hours_worked_per_week_id limit 1) as section_2_hours_worked_per_week, empls.spouse_employer as section_2_spouse_employer, empls.spouse_buisness_phone as section_2_spouse_business_phone,
            case when hcm.dependent_disabled_id = 18 then 'Yes' else 'Off' end as section_3_dependents_disabled_yes,
            case when hcm.dependent_disabled_id = 19 then 'Yes' else 'Off' end as section_3_dependents_disabled_no, hcm.dependent_disabled_name as section_3_dependents_disabled_names,
            case when hcm.dependent_insurance_other_continue_id = 18 then 'Yes' else 'Off' end as section_3_insurance_other_yes,
            case when hcm.dependent_insurance_other_continue_id = 19 then 'Yes' else 'Off' end as section_3_insurance_other_no, hcm.dependent_isu_coverage_carrier as section_3_name_of_other_health_insurance_carrier,
            hcm.effective_date as section_3_effective_date, 
            'Yes' as section_5_elect_coverage,
            'Off' as section_5_decline_coverage,
            case when hcm.coverage_level_id = 22 then 'Yes' else 'No' end as section_5_employee_only,
            case when hcm.coverage_level_id = 23 then 'Yes' else 'No' end as section_5_employee_spouse ,
            case when hcm.coverage_level_id = 24 then 'Yes' else 'No' end as section_5_employee_children ,
            case when hcm.coverage_level_id = 25 then 'Yes' else 'No' end as section_5_family,
            '' as section_5_reason_for_decline
            
            from employees empls
            inner join employers emplr on emplr.id = empls.fk_employer_id
            inner join healthquestionaire_coveragemodel hcm on hcm.employee_id = empls.id 
            where empls.id = """ + str(employee_id) + """ order by hcm.effective_date desc limit 1 """
        # sql = """
        #     select emplr.name as section_1_employer_name, emplr.street as section_1_street_address, emplr.city as section_1_city, emplr.state as section_1_state, emplr.zip_code as section_1_zip,
        #     empls.empl_first_name || ' ' || empls.empl_last_name as section_2_employee_full_name, empls.empl_hire_date assection_2_hire_date, empls.empl_dob as section_2_employee_birth_date,
        #     empls.street as section_2_street_address, empls.city as section_2_city, empls.state as section_2_state, empls.zip_code as section_2_zip,
        #     empls.empl_ssn as section_2_employee_ssn, empls.empl_gender_id as section_2_gender, case when hcm.tobacco_use_id = 18 then 'Yes' else 'No' end as section_2_tobacco_use_yes, case when hcm.tobacco_use_id = 19 then 'Yes' else 'No' end as section_2_tobacco_use_no,
        #     case when empls.marital_status_id = 26 then 'Yes' else 'No' end as section_2_marital_status_married ,
        #     case when empls.marital_status_id = 27 then 'Yes' else 'No' end as section_2_marital_status_single,
        #     case when empls.marital_status_id = 28 then 'Yes' else 'No' end as section_2_marital_status_widowed,
        #     case when empls.marital_status_id = 29 then 'Yes' else 'No' end as section_2_marital_status_divorced,
        #     empls.home_phone as section_2_home_phone, empls.cell_phone as section_2_cell_phone, empls.email_address as section_2_email_address,
        #     empls.job_title as section_2_job_title, empls.hours_worked_per_week as section_2_hours_worked_per_week, empls.spouse_employer as section_2_spouse_employer, empls.spouse_buisness_phone as section_2_spouse_business_phone,
        #     case when hcm.dependent_disabled_id = 18 then 'Yes' else 'Off' end as section_3_dependents_disabled_yes,
        #     case when hcm.dependent_disabled_id = 19 then 'Yes' else 'Off' end as section_3_dependents_disabled_no, hcm.dependent_disabled_name as section_3_dependents_disabled_names,
        #     case when hcm.dependent_insurance_other_continue_id = 18 then 'Yes' else 'Off' end as section_3_insurance_other_yes,
        #     case when hcm.dependent_insurance_other_continue_id = 19 then 'Yes' else 'Off' end as section_3_insurance_other_no, hcm.dependent_isu_coverage_carrier as section_3_name_of_other_health_insurance_carrier,
        #     hcm.effective_date as section_3_effective_date, 
        #     case when hcm.coverage_id = 20 then 'Yes' else 'Off' end as section_5_elect_coverage,
        #     case when hcm.coverage_id = 21 then 'Yes' else 'Off' end as section_5_decline_coverage,
        #     case when hcmcl.lookupmodel_id = 22 then 'Yes' else 'No' end as section_5_employee_only,
        #     case when hcmcl.lookupmodel_id = 23 then 'Yes' else 'No' end as section_5_employee_spouse ,
        #     case when hcmcl.lookupmodel_id = 24 then 'Yes' else 'No' end as section_5_employee_children ,
        #     case when hcmcl.lookupmodel_id = 25 then 'Yes' else 'No' end as section_5_family,
        #     case when hcmdr.lookupmodel_id = 30 then 'Yes' else 'No' end as section_5_spouse_employer_plan,
        #     case when hcmdr.lookupmodel_id = 31 then 'Yes' else 'No' end as section_5_individual_plan ,
        #     case when hcmdr.lookupmodel_id = 32 then 'Yes' else 'No' end as section_5_medicare ,
        #     case when hcmdr.lookupmodel_id = 33 then 'Yes' else 'No' end as section_5_medicaid,
        #     case when hcmdr.lookupmodel_id = 34 then 'Yes' else 'No' end as section_5_cobra_from_previous_employer,
        #     case when hcmdr.lookupmodel_id = 35 then 'Yes' else 'No' end as section_5_va_eligibility,
        #     case when hcmdr.lookupmodel_id = 36 then 'Yes' else 'No' end as section_5_no_other_coverage_at_this_time,
        #     case when hcmdr.lookupmodel_id = 37 then 'Yes' else 'No' end as section_5_other,
        #     hcm.others as section_5_reason_for_decline
            
        #     from employees empls
        #     inner join employers emplr on emplr.id = empls.fk_employer_id
        #     inner join healthquestionaire_coveragemodel hcm on hcm.employee_id = empls.id 
        #     inner join healthquestionaire_coveragemodel_coverage_level hcmcl on hcmcl.coveragemodel_id = hcm.id
        #     left outer join healthquestionaire_coveragemodel_decline_reasons hcmdr on hcmdr.coveragemodel_id = hcm.id
        #     where emplr_emply.employeemodel_id = """ + str(employee_id) + """ order by hcm.effective_date desc limit 1 """
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
                case when hdi.dependent_pregnant_id = 19 then 'Yes' else 'No' end as section_6_question_6_no,
                hdi.self_height_feet as section_6_employee_height_feet, hdi.self_weight_lbs as section_6_employee_weight,
                hdi.spouse_height_feet as section_6_spouse_height_feet, hdi.spouse_weight_lbs as section_6_spouse_weight 
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
                idx = 1
                for row_item in data_med_info:
                    for (key, value) in row_item.items():
                        pdf_data[''.join([key,'_', str(idx)])] = value
                    idx += 1
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
                idx = 1
                for row_item in data_med_info:
                    for (key, value) in row_item.items():
                        pdf_data[''.join([key,'_', str(idx)])] = value
                    idx += 1
            
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
                idx = 1
                for row_item in data_med_info:
                    for (key, value) in row_item.items():
                        pdf_data[''.join([key,'_', str(idx)])] = value
                    idx += 1
            
            pdf_data['signature_date_af_date'] = date.today()
            write_fillable_pdf(''.join([settings.STATIC_URL, 'media/pdf-templates/', 'LHP_Employee_Health_Application_2019(120618)(Fillable).pdf']), ''.join(['/tmp/', str(employee_id), '.pdf']), pdf_data)
        except Exception as ex:
            print(ex, 'ERror writing pdf')
        finally:
            cursor.close()
            return pdf_data


def upload_file_to_s3(uploadfile, object_name, s3_dir='static/media/submitted/'):
    
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    if object_name is None:
        object_name = uploadfile
    
    try:
        # s3 = boto3.resource('s3')
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        print(uploadfile, bucket_name, ''.join([object_name,'.pdf']))
        # s3.meta.client.upload_file(uploadfile, bucket_name, ''.join([object_name,'.pdf']), ExtraArgs={'ACL':'public-read'}) 
        # print(response)
        s3_client.upload_file(uploadfile, bucket_name, ''.join([s3_dir,object_name,'.pdf']), ExtraArgs={'ACL':'public-read'})
        # print(response)
    except ClientError as e:
        print(e, 'upload file to s3 error')
        return False
    except Exception as ex:
        print(ex, 'upload file failed')
        return False
    return True