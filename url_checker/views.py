from django.shortcuts import render
from .models import UrlStatus
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='/accounts/login/')
def main_page(request):
    query = UrlStatus.objects.all()
    return render(request, 'base.html', context={"urls": query})


def check_url_status(request):
    pass
