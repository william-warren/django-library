# Generated by Django 2.2.5 on 2019-11-08 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('author', models.TextField()),
                ('published', models.DateTimeField()),
                ('genre', models.TextField()),
                ('in_stock', models.BooleanField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('action', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Book')),
            ],
        ),
    ]
