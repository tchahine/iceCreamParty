# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def init_data_flavour(apps, schema_editor):
    Flavour = apps.get_model("vm", "Flavour")
    db_alias_flavour = schema_editor.connection.alias
    Flavour.objects.using(db_alias_flavour).bulk_create([
        Flavour(name="Chocolat Orange", picture_name="chocolat-orange.png"),
        Flavour(name="Sirop d'érable Noix", picture_name="maple-walnut.png"),
        Flavour(name="Menthe Chocolat", picture_name="mint-chocolat.png"),
        Flavour(name="Vanille Fraise Chocolat", picture_name="strawberry-vanille-chocolate.png"),
        Flavour(name="Chocolat blanc Framboise", picture_name="white-chocolate-raspberry.png"),
    ])


class Migration(migrations.Migration):
    dependencies = [
        ('vm', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            init_data_flavour,
        ),
    ]
