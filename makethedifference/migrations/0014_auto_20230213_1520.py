# Generated by Django 3.2.16 on 2023-02-13 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makethedifference', '0013_auto_20230213_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
    ]
