# Generated by Django 3.1.1 on 2020-12-07 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Post', '0001_initial'),
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='Post.post')),
                ('renter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renter', to='Account.renter')),
            ],
        ),
    ]
