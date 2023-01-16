from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('demand/', demand, name='demand'),
    path('geography/', geography, name='geography'),
    path('skills/', skills, name='skills'),
    path('vacancies/', vacancies, name='vacancies'),
]
