# Generated by Django 3.2 on 2021-04-18 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction_secondchallenge', '0002_auto_20210418_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_amount', models.FloatField()),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('requester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requester', to='transaction_secondchallenge.account')),
            ],
        ),
    ]