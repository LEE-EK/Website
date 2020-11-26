# Generated by Django 2.2.6 on 2020-11-18 15:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20200126_0047'),
        ('board', '0016_inquiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.Inquiry')),
            ],
        ),
    ]
