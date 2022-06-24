from django.urls import path
from accounts.views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]