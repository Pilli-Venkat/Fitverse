# Generated by Django 5.1.1 on 2024-10-17 03:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymDetails', '0007_gymownercreatedmembership'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymownercreatedmembership',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 10, 17, 3, 40, 30, 416078, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gymownercreatedmembership',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gymownercreatedmembership',
            name='membership_option',
            field=models.CharField(choices=[('cardio', 'Cardio'), ('strength', 'Strength Training')], default='strength', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gymownercreatedmembership',
            name='membership_type',
            field=models.CharField(choices=[('day', 'Day'), ('weekly', 'Weekly'), ('half_month', 'Half-Month'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually')], max_length=10),
        ),
        migrations.AlterField(
            model_name='gymownercreatedmembership',
            name='start_date',
            field=models.DateField(),
        ),
    ]