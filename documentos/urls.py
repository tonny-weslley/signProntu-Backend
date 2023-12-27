from django.urls import path
from .views import DocumentoViewSet, documentSignViewSet, generatePdfViewSet

urlpatterns = [
    path('/', DocumentoViewSet.as_view({ 'post': 'create', 'get': 'list'})),
    path('/<int:pk>/', DocumentoViewSet.as_view({'delete': 'destroy'})),
    path('/sign/', documentSignViewSet.as_view({'post': 'create'})),
    path('/generatePdf/', generatePdfViewSet.as_view({'post': 'create'})),
]