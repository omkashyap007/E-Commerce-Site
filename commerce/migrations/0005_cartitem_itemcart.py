# Generated by Django 4.0.4 on 2022-07-09 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0004_alter_cartitem_price_alter_cartitem_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='itemcart',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='commerce.cart'),
            preserve_default=False,
        ),
    ]
