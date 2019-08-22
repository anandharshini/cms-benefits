from crudbuilder.abstract import BaseCrudBuilder

from .models import Employer

class EmployerCrud(BaseCrudBuilder):
    model = Employer
    search_fields = ['name']
    tables2_fields = ('name', 'street', 'address2','city','state','zip_code',)
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 10  # default is 10
    modelform_excludes = []
    login_required = True
    permission_required = True
    # custom_table2 = CustomPersonTable

    # detailview_excludes = ['img']
    # inlineformset = PersonEmploymentInlineFormset

    custom_templates = {
        'list': 'employer_list.html'
    }

    # permissions = {
    #     'list': 'employer.person_list',
    #     'create': 'example.person_create'
    # }

    # @classmethod
    # def custom_queryset(cls, request, **kwargs):
    #     return cls.model.objects.filter(created_by=request.user)
