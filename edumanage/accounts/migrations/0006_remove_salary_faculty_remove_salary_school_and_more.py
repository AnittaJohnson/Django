# Generated by Django 5.1 on 2024-10-22 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_dues_fee_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salary',
            name='faculty',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='school',
        ),
        migrations.RenameField(
            model_name='fee',
            old_name='amount_due',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='fee',
            name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='fee',
            name='school',
        ),
        migrations.RemoveField(
            model_name='fee',
            name='status',
        ),
        migrations.AddField(
            model_name='fee',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Dues',
        ),
        migrations.DeleteModel(
            name='Salary',
        ),
    ]