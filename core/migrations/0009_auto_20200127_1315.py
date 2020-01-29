# Generated by Django 3.0.2 on 2020-01-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200122_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mergerequest',
            name='repo',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='mergerequest',
            name='source_branch',
            field=models.CharField(choices=[], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='mergerequest',
            name='target_branch',
            field=models.CharField(choices=[], default='', max_length=100),
        ),
    ]
