# Generated by Django 4.2.6 on 2023-10-26 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_users_phone_alter_users_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='language',
            field=models.CharField(choices=[('en', 'english'), ('fr', 'french')], default='en', max_length=10),
        ),
    ]