# Generated by Django 3.2.9 on 2021-12-03 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0007_auto_20211203_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='course_sales',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
