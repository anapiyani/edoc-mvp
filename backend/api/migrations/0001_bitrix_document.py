from django.db import migrations, models
import api.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='BitrixDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deal_id', models.CharField(db_index=True, max_length=255)),
                ('doc_id', models.CharField(db_index=True, max_length=255)),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('iin', models.CharField(blank=True, max_length=20)),
                ('file', models.FileField(max_length=500, upload_to='bitrix_documents/%Y/%m/')),
                ('token', models.CharField(default=api.models.generate_document_token, editable=False, max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Bitrix document',
                'verbose_name_plural': 'Bitrix documents',
                'ordering': ['-created_at'],
            },
        ),
    ]
