from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url, include
from form_application.views import ApplicationModelListView
from healthquestionaire.views import create_medical_model_form, create_medication_model_form, coverageview, dependentinfoview
from employer.views import employerview, edit
from django.contrib.auth.decorators import login_required
from core.views import create_dependents_model_form, signatureview

@apphook_pool.register  # register the application
class PdfPluginApp(CMSApp):
    app_name = "pdf_cms_integration"
    name = _("PDF Plugin Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', login_required(ApplicationModelListView.as_view())),
            # url(r'^questions/', login_required(HealthQuestionView.as_view(HealthQuestionView.FORMS))),
            # url(r'^employer/$', login_required(include('employer.urls'))),
            # url('^employer/edit/<int:pk>/', edit, name='employer_edit'),
            # url('^employer/create/', employerview, name='employer_create'),
            url(r'^coverage/', login_required(coverageview)),
            url(r'^dependents/', login_required(create_dependents_model_form)),
            url(r'^medicals/', login_required(create_medical_model_form)),
            url(r'^medications/', login_required(create_medication_model_form)),
            url(r'^dependentinfo/', login_required(dependentinfoview)),
            url(r'^signpdf/', login_required(signatureview)),
        ]
