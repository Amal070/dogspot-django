# Generated by Django 5.0.1 on 2024-02-04 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_missing_case_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missing_case',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]
