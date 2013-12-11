# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('inventory', '0004_order_pending')]

    operations = [
        migrations.AddField(
            field = models.BooleanField(default=False),
            name = 'completed',
            model_name = 'order',
        ),
        migrations.RemoveField(
            name = 'pending',
            model_name = 'order',
        ),
    ]
