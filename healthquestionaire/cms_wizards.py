from cms.wizards.wizard_base import Wizard
from cms.wizards.wizard_pool import wizard_pool

from .forms import HealthApplicationForm, EmployeeForm, EmployeeFormset
from .models import EmployeeModel

class HealthAppWizard(Wizard):
    def get_success_url(self, obj, **kwargs):
        """
        This should return the URL of the created object, «obj».
        """
        # if 'language' in kwargs:
        #     url = obj.get_absolute_url()
        # else:
        url = obj.get_absolute_url()

        return url

health_app_wizard = HealthAppWizard(
    title="Health Questionnaire",
    weight=200,
    form=EmployeeFormset,
    model=EmployeeModel,
    description="Create a new Health Questions instance",
)

wizard_pool.register(health_app_wizard)
