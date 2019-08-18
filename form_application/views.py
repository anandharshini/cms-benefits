from django.views.generic.list import ListView

from .models import ApplicationModel
from core.models import LookupModel
from healthquestionaire.models import EmployeeModel
from core.utils import check_signed_file_exists
from healthquestionaire.views import get_employee_instance
from django.conf import settings

class ApplicationModelListView(ListView):
    model = ApplicationModel
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        self.request.session.set_expiry(settings.SESSION_EXPIRY_TIME)
        context = super(ApplicationModelListView, self).get_context_data(**kwargs)
        # context["submitted_apps"] = LookupModel.objects.all()
        employee = get_employee_instance(self.request.user, self.request.GET.get('employee', None))
        # print(employee, 'check signed file')
        context['check_signed_file'] = check_signed_file_exists(employee.id) if employee else False
        context['employee'] = employee
        context["application_exist"] = EmployeeModel.objects.filter(login_user=self.request.user)
        return context
