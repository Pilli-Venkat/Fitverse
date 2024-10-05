# Generated by Django 5.1.1 on 2024-10-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('gym_owner', 'Gym Owner'), ('customer', 'Customer'), ('trainer', 'Trainer')], default='customer', max_length=15),
        ),
    ]
