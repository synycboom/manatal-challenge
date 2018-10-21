# Generated by Django 2.1.2 on 2018-10-21 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('max_students', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('identification', models.CharField(editable=False, max_length=20, unique=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='education.School')),
            ],
        ),
    ]
