# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('inventory', '0001_initial')]

    operations = [
        migrations.AddField(
            field = models.CharField(default='', max_length=100, blank=True),
            name = 'employee_name',
            model_name = 'order',
        ),
        migrations.AddField(
            field = models.CharField(default='', max_length=100, blank=True),
            name = 'job_name',
            model_name = 'order',
        ),
        migrations.AlterField(
            field = models.ForeignKey(to=u'inventory.Employee', to_field=u'id', null=True),
            name = 'employee',
            model_name = 'order',
        ),
        migrations.AlterField(
            field = models.TextField(default='', blank=True),
            name = 'message',
            model_name = 'order',
        ),
        migrations.AlterField(
            field = models.ForeignKey(to=u'inventory.Job', to_field=u'id', null=True),
            name = 'job',
            model_name = 'order',
        ),
    ]
