from django.urls import path

from . import views

app_name = "qrcodes"
urlpatterns = [
    # ex: /qr/5/
    path("show/<str:type>/<str:qr_id>/", views.qr_img, name="detail"),
    path("new/", views.new_qr, name="newqr"),
    path("generate/", views.generate_qr, name="singleqr"),
    path("new/webQR/", views.new_web_qr, name="new_web_qr"),
    path("new/vcardQR/", views.new_vcard_qr, name="new_vcard_qr"),
    path("new/wifiQR/", views.new_wifi_qr, name="new_wifi_qr"),
    path("details/<str:type>/<str:qr_id>/", views.details, name="details"),
]

