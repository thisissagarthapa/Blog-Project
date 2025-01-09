from django.urls import path
from .views import RegisterApiView,LoginApiView,LogoutApiView
urlpatterns = [
    path('register/',RegisterApiView.as_view(),name='register'),
    path('login/',LoginApiView.as_view(),name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'), ]
