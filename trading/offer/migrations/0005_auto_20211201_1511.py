# Generated by Django 3.2.9 on 2021-12-01 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offer', '0004_alter_trade_currenc'),
    ]

    operations = [
        migrations.AddField(
            model_name='money',
            name='currenc',
            field=models.ForeignKey(blank=True, max_length=15, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offer.currency'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='authentication.user'),
        ),
        migrations.AlterField(
            model_name='money',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallets', to='authentication.user'),
        ),
    ]
