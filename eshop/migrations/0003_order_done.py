# Generated by Django 5.1.4 on 2025-01-04 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
