# Generated by Django 4.1.7 on 2023-06-09 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SecretNotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secretnote',
            name='note',
            field=models.TextField(),
        ),
    ]