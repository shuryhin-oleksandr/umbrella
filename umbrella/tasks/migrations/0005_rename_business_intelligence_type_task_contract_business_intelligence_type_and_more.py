# Generated by Django 4.0.1 on 2022-03-25 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_business_intelligence_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='business_intelligence_type',
            new_name='contract_business_intelligence_type',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='clause_type',
            new_name='contract_clause_type',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='link_to_text',
            new_name='link_to_contract_text',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='repeats',
            new_name='reminder_repeats',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='until',
            new_name='reminder_until',
        ),
    ]
