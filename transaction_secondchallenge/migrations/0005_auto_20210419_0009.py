# Generated by Django 3.2 on 2021-04-18 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction_secondchallenge', '0004_paymentrequest_requested_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='attachment',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(),
        ),
    ]
