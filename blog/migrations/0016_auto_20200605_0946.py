# Generated by Django 3.0.6 on 2020-06-05 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='email_address',
            field=models.EmailField(blank=True, max_length=500, verbose_name='e-mail адрес для ответа'),
        ),
    ]
