# Generated by Django 4.2.13 on 2024-06-24 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="students",
            field=models.ManyToManyField(related_name="groups", to="journal.student"),
        ),
        migrations.AlterField(
            model_name="group",
            name="leader",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="leader",
                to="journal.student",
            ),
        ),
    ]
