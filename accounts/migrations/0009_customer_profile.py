# Generated by Django 3.0.3 on 2020-03-02 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200301_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
