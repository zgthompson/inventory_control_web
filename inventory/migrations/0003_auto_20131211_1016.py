# encoding: utf8
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):
    
    dependencies = [('inventory', '0002_auto_20131211_0929')]

    operations = [
        migrations.AddField(
            field = models.DateTimeField(default=datetime.datetime.now, verbose_name='date ordered'),
            name = 'date_ordered',
            model_name = 'order',
        ),
        migrations.AlterField(
            field = models.ForeignKey(to_field=u'id', blank=True, to=u'inventory.Employee', null=True),
            name = 'employee',
            model_name = 'order',
        ),
        migrations.AlterField(
            field = models.ForeignKey(to_field=u'id', blank=True, to=u'inventory.Job', null=True),
            name = 'job',
            model_name = 'order',
        ),
    ]
