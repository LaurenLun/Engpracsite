# Generated by Django 5.0.6 on 2024-10-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='username',
            new_name='usname',
        ),
        migrations.AlterField(
            model_name='users',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
