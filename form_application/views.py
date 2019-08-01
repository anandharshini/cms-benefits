from django.views.generic.list import ListView

from .models import ApplicationModel
from core.models import LookupModel
from healthquestionaire.models import EmployeeModel

class ApplicationModelListView(ListView):
    model = ApplicationModel
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super(ApplicationModelListView, self).get_context_data(**kwargs)
        # context["submitted_apps"] = LookupModel.objects.all()
        context["application_exist"] = EmployeeModel.objects.filter(login_user=self.request.user)
        return context
