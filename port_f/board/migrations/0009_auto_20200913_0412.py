# Generated by Django 2.2.6 on 2020-09-12 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_from_mark_from_mark_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='from_mark',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
