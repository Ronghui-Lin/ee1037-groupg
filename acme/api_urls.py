from django.urls import path
from . import api_views

urlpatterns = [
    path('signin/', api_views.api_signin, name='api_signin'),
    path('signup/', api_views.api_signup, name='api_signup'),
    path('user/', api_views.user_details, name='api_user_details'),
    path('logout/', api_views.logout, name='api_logout'),
]