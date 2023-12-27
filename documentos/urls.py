from django.urls import path
from .views import DocumentoViewSet, documentSignViewSet

urlpatterns = [
    path('/', DocumentoViewSet.as_view({ 'post': 'create'})),
    path('/<int:pk>/', DocumentoViewSet.as_view({'delete': 'destroy'})),
    path('/sign/', documentSignViewSet.as_view({'post': 'create'})),
]