# Generated by Django 4.0.2 on 2022-04-19 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_delete_lease_contract_created_by_contract_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clause',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('contracts.node',),
        ),
        migrations.CreateModel(
            name='KDP',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('contracts.node',),
        ),
        migrations.AlterField(
            model_name='node',
            name='clause',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kdps', to='contracts.node'),
        ),
        migrations.AlterField(
            model_name='node',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clauses', to='contracts.contract'),
        ),
    ]
