# Generated by Django 3.2.9 on 2021-11-30 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
