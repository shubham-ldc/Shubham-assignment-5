from django.urls import path 
from . import views

urlpatterns = [
    path('signup',views.UserSignupApiView.as_view(),name="UserSignupApiView" ),
    path('login',views.UserLoginApiView.as_view(),name="UserLoginApiView" ),
    path('get-user-scheme',views.GetUserschemeApiView.as_view(),name="GetUserschemeApiView" ),
    path('get-user-post',views.GetUserpostApiView.as_view(),name="GetUserschemeApiView" ),
    path('get-user-portfolio',views.GetUserPortfolio.as_view(),name="GetUserPortfolio" ),
]