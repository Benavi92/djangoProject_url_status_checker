import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import UrlStatus
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from requests import request as r
from asgiref.sync import sync_to_async, async_to_sync
from django.core import serializers
import json

import asyncio
import aiohttp
from aiohttp import ClientConnectorCertificateError, ServerConnectionError, ClientConnectorError

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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

    obj = await sync_to_async(UrlStatus.objects.get)(url=url)
    obj.status_code = status_code
    await sync_to_async(obj.save)(update_fields=["status_code"])


async def start_async_requests(urls):
    c = []
    async with aiohttp.ClientSession() as client:
        for i in urls:
            c.append(asyncio.create_task(do_request(client, i)))
        await asyncio.gather(*c)


@login_required(login_url='/accounts/login/')
def main_page(request):
    query = UrlStatus.objects.all()
    return render(request, 'base.html', context={"urls": query})


# def check_url_status(request, pk):
#     try:
#         status_code = r("GET", pk, timeout=2).status_code
#     except requests.Timeout:
#         status_code = 0
#
#     obj = get_object_or_404(UrlStatus, url=pk)
#     obj.status_code = status_code
#     obj.save(update_fields=status_code)
#
#     return JsonResponse({"status_code": status_code})

async def check_all(request):
    query = await sync_to_async(list)(UrlStatus.objects.all())  # UrlStatus.objects.all()

    body = json.loads(request.body)

    do_not_update = body.get("to_not_update", [])

    urls = [u.url for u in query if u.pk not in do_not_update]
    print(urls)
    await start_async_requests(urls)
    result = await sync_to_async(list)(UrlStatus.objects.all())

    resp = []
    for row in result:
        resp.append({
            "pk": row.pk,
            "url": row.url,
            "status_code": row.status_code
        })

    return JsonResponse({"to_update": resp})


