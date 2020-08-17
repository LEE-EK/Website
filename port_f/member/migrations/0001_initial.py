# Generated by Django 2.2.6 on 2019-12-06 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=50)),
                ('member_pw', models.CharField(max_length=200)),
                ('nickname', models.CharField(max_length=50)),
                ('member_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200, blank=True)),
                ('address_in', models.CharField(max_length=200, blank=True)),
                ('phone_no', models.CharField(max_length=100, blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('member_date', models.DateField(auto_now_add=True, verbose_name='join_date')),
            ],
        ),
    ]
