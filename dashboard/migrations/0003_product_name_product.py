# Generated by Django 4.1.7 on 2023-05-21 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_rename_amount_sales_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name_product',
            field=models.CharField(default='', max_length=80),
            preserve_default=False,
        ),
    ]
