from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_management', '0002_staff_blood_group_staff_marital_status_and_more'),
    ]

    operations = [
        # Remove IFSC code
        migrations.RemoveField(
            model_name='staff',
            name='ifsc_code',
        ),
        # Replace Aadhar with National ID
        migrations.RemoveField(
            model_name='staff',
            name='aadhar_number',
        ),
        # Replace PAN with KRA PIN
        migrations.RemoveField(
            model_name='staff',
            name='pan_number',
        ),
        # Add Kenyan-specific fields
        migrations.AddField(
            model_name='staff',
            name='bank_branch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='national_id',
            field=models.CharField(blank=True, help_text='Kenya national ID (8 digits)', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='kra_pin',
            field=models.CharField(blank=True, help_text='Kenya Revenue Authority PIN', max_length=15, null=True),
        ),
        # Update nationality default
        migrations.AlterField(
            model_name='staff',
            name='nationality',
            field=models.CharField(blank=True, default='Kenyan', max_length=50),
        ),
    ]
