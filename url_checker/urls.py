from django.urls import path
from .views import main_page, check_all

urlpatterns = [
    path('', main_page),
    path('check_all/', check_all),
]
