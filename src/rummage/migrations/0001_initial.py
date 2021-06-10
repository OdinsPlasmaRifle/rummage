# Generated by Django 3.0.4 on 2021-04-12 10:00

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enumfields.fields
import rummage.enums
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('identifier', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('retries', models.IntegerField(default=0)),
                ('exceptions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), blank=True, default=list, null=True, size=None)),
                ('status', enumfields.fields.EnumField(db_index=True, default='queued', enum=rummage.enums.SearchStatus, max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.CharField(db_index=True, max_length=250, unique=True)),
                ('enabled', models.BooleanField(db_index=True, default=True)),
                ('website', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('term', models.CharField(db_index=True, max_length=150)),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='rummage.Search')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(max_length=250)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=dict, null=True)),
                ('expires', models.DateTimeField()),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rummage.Store')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='rummage.SearchTerm')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='SearchError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('error', models.CharField(max_length=250)),
                ('expires', models.DateTimeField()),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rummage.Store')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='errors', to='rummage.SearchTerm')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.AddField(
            model_name='search',
            name='stores',
            field=models.ManyToManyField(to='rummage.Store'),
        ),
    ]