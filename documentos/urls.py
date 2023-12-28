from django.urls import path, include
from .views import DocumentoViewSet, DocumentVerifyViewSet



urlpatterns = [
    path('/', DocumentoViewSet.as_view({ 'post': 'createAndSign', 'get': 'list'})),
    path('/verify_hash/<str:hash>', DocumentVerifyViewSet.as_view({ 'get': 'verify'})),
]