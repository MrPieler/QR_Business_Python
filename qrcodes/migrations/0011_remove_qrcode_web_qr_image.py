# Generated by Django 2.2 on 2019-05-31 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qrcodes', '0010_auto_20190531_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrcode_web',
            name='qr_image',
        ),
    ]
