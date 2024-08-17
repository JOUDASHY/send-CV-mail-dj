from django.urls import path
from . import views

urlpatterns = [
	path('', views.index),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('mail_entreprise/<str:entreprise>/<str:mail_entreprise>', views.mail_entreprise,name="mail_entreprise"),
    
]
