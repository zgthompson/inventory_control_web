# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = []

    operations = [
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('name', models.CharField(unique=True, max_length=100),), ('units', models.CharField(max_length=20),), ('quantity', models.IntegerField(default=0),), ('price', models.DecimalField(max_digits=7, decimal_places=2),)],
            bases = (models.Model,),
            options = {},
            name = 'Item',
        ),
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('name', models.CharField(max_length=100),), ('number', models.CharField(unique=True, max_length=20),)],
            bases = (models.Model,),
            options = {},
            name = 'Job',
        ),
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('name', models.CharField(unique=True, max_length=100),)],
            bases = (models.Model,),
            options = {},
            name = 'Employee',
        ),
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('employee', models.ForeignKey(to=u'inventory.Employee', to_field=u'id'),), ('job', models.ForeignKey(to=u'inventory.Job', to_field=u'id'),), ('message', models.TextField(),)],
            bases = (models.Model,),
            options = {},
            name = 'Order',
        ),
        migrations.CreateModel(
            fields = [(u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True),), ('order', models.ForeignKey(to=u'inventory.Order', to_field=u'id'),), ('item', models.ForeignKey(to=u'inventory.Item', to_field=u'id'),), ('quantity', models.IntegerField(),)],
            bases = (models.Model,),
            options = {},
            name = 'LineItem',
        ),
    ]
