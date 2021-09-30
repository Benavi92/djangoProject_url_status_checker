from django.urls import path
from .views import main_page, check_url_status

urlpatterns = [
    path('', main_page),
    path('check/<url>', check_url_status)

]
