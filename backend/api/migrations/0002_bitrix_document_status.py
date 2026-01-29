# Generated manually: add status field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_bitrix_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitrixdocument',
            name='status',
            field=models.CharField(
                choices=[
                    ('awaiting_decision', 'awaiting_decision'),
                    ('accepted', 'accepted'),
                    ('rejected', 'rejected'),
                ],
                db_index=True,
                default='awaiting_decision',
                max_length=20,
            ),
        ),
    ]
