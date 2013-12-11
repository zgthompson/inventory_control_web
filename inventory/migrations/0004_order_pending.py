# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):
    
    dependencies = [('inventory', '0003_auto_20131211_1016')]

    operations = [
        migrations.AddField(
            field = models.BooleanField(default=True),
            name = 'pending',
            model_name = 'order',
        ),
    ]
