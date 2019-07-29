from .models import EmployeeModel
from employer.models import Employer
from core.models import Address
from form_application.models import ApplicationModel
from django.core.exceptions import ValidationError

def process_data(request, data):
    # Process Employer
    try:
        employer = Employer.objects.get(name=data[0]['name'])
    except (Employer.DoesNotExist):
        empl_address = Address(
            street=data[0]['street'],
            city=data[0]['city'],
            state=data[0]['state'],
            zip_code=data[0]['zip_code'],
            address_type=data[0]['address_type']
        )
        empl_address.save()
        employer = Employer(name=data[0]['name'], employer_address=empl_address)
        try:
            employer.full_clean()
            employer.save()
        except ValidationError as e:
            print(e, 'employer error')
    # Process Employee
    try:
        employee = EmployeeModel.objects.get(empl_ssn=data[1]['empl_ssn'])
    except (EmployeeModel.DoesNotExist):
        try:
            empl_address = Address.objects.get(street=data[1]['street'], zip_code=data[1]['zip_code'])
        except (Address.DoesNotExist):
            empl_address = Address(
                street=data[1]['street'],
                city=data[1]['city'],
                state=data[1]['state'],
                zip_code=data[1]['zip_code'],
                address_type=data[1]['address_type']
            )
            empl_address.save()
        try:
            employee = EmployeeModel(
                empl_full_name = data[1]['empl_full_name'],
                empl_hire_date = data[1]['empl_hire_date'],
                empl_dob = data[1]['empl_dob'],
                empl_ssn = data[1]['empl_ssn'],
                empl_gender = data[1]['empl_gender'],
                empl_address=empl_address,
                employer=employer,
                form_type=data[1]['form_type']
            )
            employee.full_clean()
            employee.save()
        except ValidationError as e:
            print(e, 'employee creation error') 

    app_model = ApplicationModel(
        name = employee.form_type, 
        submit_user = request.user, 
        employee = employee 
    )
    try:
        app_model.full_clean()
        app_model.save()
    except ValidationError as e:
            print(e, 'app model error')
    
    return employee
