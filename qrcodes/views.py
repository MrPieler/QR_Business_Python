from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from django.urls import reverse
import json
import base64
import segno
import io
from PIL import Image

from .models import QRCode_Web, QRCode_VCard, QRCode_Wifi
from QR_Business.settings import MEDIA_ROOT, MEDIA_URL


#Method for showing specific QR code
def qr_img(request, type, qr_id):    
    qr = get_qr_object(type, qr_id)
    buff = io.BytesIO()
    qr = segno.make(qr.generate_QR())
    qr.save(buff, kind="png", scale=15)
    return HttpResponse(buff.getvalue(), content_type="image/png")


def details(request, type, qr_id): 

    qr = get_qr_object(type, qr_id)

    if request.method == "GET":
        context = {
            "qrcode": qr,
            "type": type
        }
        return render(request, f"qrcodes/qrdetails{type}.html", context)

    if request.method == "POST":
        qr.name = request.POST["name"]

        if type == "web":
            qr.url = request.POST["url"]
        elif type == "wifi":
            qr.wifiname = request.POST["wifiname"]
            qr.wifipassword = request.POST["password"]
            qr.wifitype = request.POST["type"]
        elif type == "vcard":
            qr.firstname = request.POST["firstname"]
            qr.lastname = request.POST["lastname"]
            qr.email = request.POST["email"]
            qr.phone = request.POST["phone"]

        qr.save()

        return HttpResponseRedirect(reverse('qrcodes:newqr'))

@login_required
def new_qr(request):
    if request.method == "GET":
        qrcodes_web = QRCode_Web.objects.filter(user=request.user)
        qrcodes_vcard = QRCode_VCard.objects.filter(user=request.user)
        qrcodes_wifi = QRCode_Wifi.objects.filter(user=request.user)
        context = {
            "qrcodes_web": qrcodes_web,
            "qrcodes_wifi":qrcodes_wifi,
            "qrcodes_vcard":qrcodes_vcard
        }

        return render(request, "qrcodes/newqr.html", context)

    return HttpResponseBadRequest()

@login_required
def new_web_qr(request):
    if request.method == "GET":
        return render(request, "qrcodes/qrweb.html")

    if request.method == "POST":
        qr = QRCode_Web()
        qr.name = request.POST["name"]
        qr.url = request.POST["url"]
        qr.user = request.user
        qr.save()

        return redirect(f"/qr/show/web/{qr.qr_id}")   
    return HttpResponseBadRequest()

@login_required
def new_vcard_qr(request):
    if request.method == "GET":
        return render(request, "qrcodes/qrvcard.html")

    if request.method == "POST":
        qr = QRCode_VCard()
        qr.name = request.POST["name"]
        qr.user = request.user
        qr.firstname = request.POST["firstname"]
        qr.lastname = request.POST["lastname"]
        qr.email = request.POST["email"]
        qr.phone = request.POST["phone"]
        qr.save()

        return redirect(f"/qr/show/vcard/{qr.qr_id}")
    
    return HttpResponseBadRequest()

@login_required
def new_wifi_qr(request):
    if request.method == "GET":
        return render(request, "qrcodes/qrwifi.html")

    if request.method == "POST":
        qr = QRCode_Wifi()
        qr.name = request.POST["name"]
        qr.user = request.user
        qr.wifiname = request.POST["wifiname"]
        qr.wifipassword = request.POST["password"]
        qr.wifitype = request.POST["type"]
        qr.save()

        return redirect(f"/qr/show/wifi/{qr.qr_id}")
    
    return HttpResponseBadRequest()


@api_view(["GET"])
def generate_qr(request):    
    
    if request.GET.get("type", "") == "web":
        qr = QRCode_Web
        qr.url = request.GET.get("url", "")
    
    elif request.GET.get("type", "") == "vcard":
        qr = QRCode_VCard
        qr.firstname = request.GET.get("firstname", "")
        qr.lastname = request.GET.get("lastname", "")
        qr.email = request.GET.get("email", "")
        qr.phone = request.GET.get("number", "")

    elif request.GET.get("type", "") == "wifi":
        qr = QRCode_Wifi
        qr.wifiname = request.GET.get("wifiname", "")
        qr.wifipassword = request.GET.get("wifipassword", "")
        qr.wifitype = request.GET.get("wifitype", "")
 
    if qr:
        buff = io.BytesIO()
        qr = segno.make(qr.generate_QR(qr))
        qr.save(buff, kind="png", scale=15)
        return Response(base64.b64encode(buff.getvalue()))

    return HttpResponseNotFound

def get_qr_object(type, qr_id):
    types = {
        "web": QRCode_Web,
        "vcard": QRCode_VCard,
        "wifi": QRCode_Wifi,
    }
    qrtype = types.get(type)

    return get_object_or_404(qrtype, pk=qr_id)