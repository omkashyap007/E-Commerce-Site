# Generated by Django 4.0.4 on 2022-04-20 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_useraccount_auth_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='auth_token',
            field=models.CharField(blank=True, max_length=108, null=True),
        ),
    ]
