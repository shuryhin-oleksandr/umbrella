# Generated by Django 3.2.10 on 2021-12-23 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lease",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("file_name", models.CharField(blank=True, max_length=512, null=True)),
                ("pdf", models.BinaryField(blank=True, null=True)),
                ("txt", models.TextField(blank=True, null=True)),
                ("extracted", models.JSONField(blank=True, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("createdon", models.DateTimeField(blank=True, null=True)),
                ("createdby", models.CharField(blank=True, max_length=128, null=True)),
                ("modifiedon", models.DateTimeField(blank=True, null=True)),
                ("modifiedby", models.CharField(blank=True, max_length=128, null=True)),
                ("activeflag", models.BooleanField(blank=True, null=True)),
                (
                    "contract_type",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                ("textract", models.JSONField(blank=True, null=True)),
                ("analyticsdata", models.JSONField(blank=True, null=True)),
                ("pdf_hash", models.TextField(blank=True, null=True)),
                ("file_size", models.BigIntegerField(blank=True, null=True)),
                (
                    "modified_file_name",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("analytics2", models.JSONField(blank=True, null=True)),
                ("doc_type", models.CharField(blank=True, max_length=258, null=True)),
            ],
            options={"db_table": "lease", "managed": True},
        )
    ]