# Generated by Django 3.2.16 on 2023-02-01 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makethedifference', '0002_auto_20230201_1112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='creator',
            new_name='creator_of_event',
        ),
    ]
