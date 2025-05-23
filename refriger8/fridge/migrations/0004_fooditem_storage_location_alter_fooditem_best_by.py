# Generated by Django 5.2 on 2025-04-07 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fridge', '0003_alter_fooditem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='storage_location',
            field=models.CharField(choices=[('fridge', 'Fridge'), ('freezer', 'Freezer'), ('upper_pantry', 'Upper Pantry'), ('lower_pantry', 'Lower Pantry'), ('counter', 'Counter'), ('candy_cabinet', 'Candy Cabinet'), ('hanging_table', 'Hanging Table'), ('bar', 'Bar')], default='fridge', max_length=50),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='best_by',
            field=models.DateField(blank=True, null=True),
        ),
    ]
