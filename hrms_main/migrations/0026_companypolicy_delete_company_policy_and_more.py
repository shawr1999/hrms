# Generated by Django 5.0.6 on 2024-07-24 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_main', '0025_module_permission_role_rolepermission_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='policies/')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrms_main.branch')),
            ],
        ),
        migrations.DeleteModel(
            name='Company_Policy',
        ),
        migrations.AlterField(
            model_name='rolepermission',
            name='role',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='hrms_main.role'),
        ),
    ]
