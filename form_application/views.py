from django.views.generic.list import ListView

from .models import ApplicationModel

class ApplicationModelListView(ListView):
    model = ApplicationModel
    paginate_by = 20
