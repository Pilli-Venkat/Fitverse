# Generated by Django 5.1.1 on 2024-10-15 07:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymDetails', '0006_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='GymOwnerCreatedMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('start_date', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('membership_type', models.CharField(choices=[('day', 'Day'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually')], max_length=10)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships_created_by_owners', to='gymDetails.gyminfo')),
            ],
        ),
    ]
