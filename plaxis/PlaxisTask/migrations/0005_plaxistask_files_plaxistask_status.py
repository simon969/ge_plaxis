# Generated by Django 4.0 on 2022-02-20 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlaxisTask', '0004_alter_plaxisdocuments_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='plaxistask',
            name='files',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='plaxistask',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
