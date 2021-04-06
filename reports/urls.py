from django.urls import path
from reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='list'),
    path('save/', views.create_report, name='save'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('<int:pk>/pdf/', views.generate_pdf_view, name='pdf'),
    path('from-file/', views.UploadTemplateView.as_view(), name='from-file'),
    path('upload/', views.csv_upload, name='upload'),
]