import django_filters
from form_application.models import ApplicationModel

class ApplicationModelFilter(django_filters.FilterSet):
    class Meta:
        model = ApplicationModel
        fields = ['form_name', 'employee', 'employee__fk_employer', ]