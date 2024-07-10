from django.urls import path 
from . import views

urlpatterns = [
    path('create-scheme',views.CreateSchemeApiView.as_view(),name="CreateSchemeApiView" ),
    path('get-all-scheme',views.GetAllSchemeApiView.as_view(),name="GetAllSchemeApiView" ),
    path('get-top-scheme',views.GetTopSchemeApiView.as_view(),name="GetTopSchemeApiView" ),
]