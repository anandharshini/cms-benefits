from django.conf.urls import url
from . import views
from form_application.views import ApplicationModelListView
from django.contrib.auth.decorators import login_required
from core.views import create_dependents_model_form, signatureview


urlpatterns = [
            url(r'^$', login_required(ApplicationModelListView.as_view())),
            # url(r'^questions/', login_required(HealthQuestionView.as_view(HealthQuestionView.FORMS))),
            # url(r'^employer/$', login_required(include('employer.urls'))),
            # url('^employer/edit/<int:pk>/', edit, name='employer_edit'),
            # url('^employer/create/', employerview, name='employer_create'),
            url(r'^coverage/', login_required(views.coverageview)),
            url(r'^dependents/', login_required(create_dependents_model_form)),
            url(r'^medicals/', login_required(views.create_medical_model_form)),
            url(r'^medications/', login_required(views.create_medication_model_form)),
            url(r'^dependentinfo/', login_required(views.dependentinfoview)),
            url(r'^signpdf/', login_required(signatureview)),
        ]
