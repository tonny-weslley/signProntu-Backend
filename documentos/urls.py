from django.urls import path, include
from .views import DocumentoViewSet, documentSignViewSet, GeneratePdfViewSet
from rest_framework import routers



urlpatterns = [
    path('/', DocumentoViewSet.as_view({ 'post': 'create', 'get': 'list'})),
    path('/<int:pk>/', DocumentoViewSet.as_view({'delete': 'destroy'})),
    path('/sign/', documentSignViewSet.as_view({'post': 'create'})),
    path('/<int:pk>/generatePdf', GeneratePdfViewSet.as_view({'get': 'generatePdf'})),
]