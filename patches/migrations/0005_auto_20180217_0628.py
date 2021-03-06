# Generated by Django 2.0.2 on 2018-02-17 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patches', '0004_auto_20180216_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='showing',
            name='topics',
            field=models.ManyToManyField(to='patches.Topic'),
        ),
    ]
