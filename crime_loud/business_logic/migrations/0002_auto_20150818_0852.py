# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_logic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginAuditLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=7)),
                ('date', models.DateTimeField()),
                ('person_id', models.ForeignKey(to='business_logic.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='leadigitalevidence',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pdeattribute',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
