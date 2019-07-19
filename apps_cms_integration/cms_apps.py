from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from form_application.views import ApplicationModelListView
from healthquestionaire.views import HealthQuestionView
from healthquestionaire.forms import HealthApplicationForm, EmployeeForm, EmployerForm
from django.contrib.auth.decorators import login_required

@apphook_pool.register  # register the application
class PdfPluginApp(CMSApp):
    app_name = "pdf_cms_integration"
    name = _("PDF Plugin Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', login_required(ApplicationModelListView.as_view())),
            url(r'^questions/', login_required(HealthQuestionView.as_view(HealthQuestionView.FORMS)))
        ]
