# Generated by Django 3.2.9 on 2021-12-01 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0003_auto_20211201_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='currenc',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
