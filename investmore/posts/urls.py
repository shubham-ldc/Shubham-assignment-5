from django.urls import path 
from . import views

urlpatterns = [
    path('create-post',views.CreatePostApiView.as_view(),name="CreatePostApiView" ),
    path('get-all-post',views.GetAllPostApiView.as_view(),name="GetAllPostApiView" )
]
