# Generated by Django 3.2.16 on 2023-02-20 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makethedifference', '0016_alter_event_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]