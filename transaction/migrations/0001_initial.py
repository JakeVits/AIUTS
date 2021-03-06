# Generated by Django 3.2 on 2021-04-09 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('acc_add', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('balance', models.FloatField(default=100.0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(default=100.0)),
                ('remark', models.TextField(blank=True, max_length=200)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='transaction.account')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='transaction.account')),
            ],
        ),
    ]
