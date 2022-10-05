# Generated by Django 4.1.1 on 2022-10-05 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='story')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_end', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StoryViewed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='story.story')),
            ],
        ),
    ]
