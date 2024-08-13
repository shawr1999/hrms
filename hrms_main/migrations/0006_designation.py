# Generated by Django 5.0.6 on 2024-07-08 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_main', '0005_department_department_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation_id', models.CharField(blank=True, max_length=255, unique=True)),
                ('designation_department', models.CharField(max_length=255)),
                ('designation_name', models.CharField(max_length=255)),
            ],
        ),
    ]
