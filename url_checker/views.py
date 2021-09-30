import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import UrlStatus
from django.contrib.auth.decorators import login_required
from requests import request as r

import asyncio
import aiohttp
from aiohttp import ClientConnectorCertificateError, ServerConnectionError, ClientConnectorError


timeout = aiohttp.ClientTimeout(connect=2)


async def do_request(client, url):
    status_code = 0
    try:
        async with client.get(url, timeout=timeout) as response:
            status_code = response.status
    except ClientConnectorCertificateError:
        status_code = 200

    except (ServerConnectionError, ClientConnectorError):
        status_code = 0

    obj = UrlStatus.objects.get(url=url)
    obj.status_code = status_code
    obj.save(update_fields=["status_code"])


async def start_async_requests(urls):
    c = []
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as client:
        for i in urls:
            c.append(asyncio.create_task(do_request(client, i)))


@login_required(login_url='/accounts/login/')
def main_page(request):
    query = UrlStatus.objects.all()
    return render(request, 'base.html', context={"urls": query})


def check_url_status(request, url):
    try:
        status_code = r("GET", url,timeout=2).status_code
    except requests.Timeout:
        status_code = 0

    obj = get_object_or_404(UrlStatus, url=url)
    obj.status_code = status_code
    obj.save(update_fields=status_code)

    return JsonResponse({"status_code": status_code})


def check_all(request):
    query = UrlStatus.objects.all()

    loop = asyncio.get_event_loop()
    urls = [u.url for u in query]

    loop.run_until_complete(start_async_requests(urls))

    result = UrlStatus.objects.all()

    return JsonResponse([u for u in result])








