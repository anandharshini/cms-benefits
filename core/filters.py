import django_filters
from form_application.models import ApplicationModel
from core.models import LookupModel

class ApplicationModelFilter(django_filters.FilterSet):
    # form_name = django_filters.ModelChoiceFilter(queryset=LookupModel.objects.filter(type_lookup='form_type'))
    class Meta:
        model = ApplicationModel
        fields = ['employee__fk_employer', ]