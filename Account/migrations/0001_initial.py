# Generated by Django 3.1.1 on 2020-12-14 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('user_type', models.CharField(choices=[('renter', 'renter'), ('host', 'host'), ('admin', 'admin')], max_length=10)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Account.myuser')),
            ],
            options={
                'abstract': False,
            },
            bases=('Account.myuser',),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Account.myuser')),
                ('fullname', models.CharField(max_length=50)),
                ('identication', models.CharField(max_length=20, unique=True)),
                ('address', models.CharField(max_length=100)),
                ('phoneNumber', models.CharField(max_length=20, unique=True)),
                ('is_confirmed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('Account.myuser',),
        ),
        migrations.CreateModel(
            name='Renter',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Account.myuser')),
                ('fullname', models.CharField(blank=True, max_length=50, null=True)),
                ('interested_area', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('Account.myuser',),
        ),
    ]
