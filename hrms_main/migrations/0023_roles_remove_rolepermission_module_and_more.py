# Generated by Django 5.0.6 on 2024-07-23 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms_main', '0022_module_permission_role_rolepermission_delete_roles_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role_name', models.CharField(max_length=255)),
                ('Module', models.CharField(max_length=255)),
                ('Permission', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='rolepermission',
            name='module',
        ),
        migrations.RemoveField(
            model_name='role',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='rolepermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='rolepermission',
            name='role',
        ),
        migrations.DeleteModel(
            name='Module',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='RolePermission',
        ),
    ]
