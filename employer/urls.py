from django.conf.urls import url
from . import views
# urlpatterns = [
#     # path('employer/', views.IndexView.as_view(), name='employer_index'),
#     # path('<int:pk>/', views.PostDetailView.as_view(), name='employer_detail'),
#     url('^edit/<int:pk>/', views.edit, name='employer_edit'),
#     url('^create/', views.employerview, name='employer_create'),
#     # path('delete/<int:pk>/', views.delete, name='employer_delete'),
# ]

urlpatterns = [
    url('edit/<int:pk>/', views.edit, name='employer_edit',),
    url('create/', views.employerview, name='employer_create',),
]