# Generated by Django 3.0.4 on 2020-04-02 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('middle_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('aadhar', models.CharField(max_length=12, unique=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('constitucy', models.CharField(blank=True, max_length=255, null=True)),
                ('ward', models.CharField(blank=True, max_length=255, null=True)),
                ('landmark', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], default=None, max_length=20, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('role', models.CharField(blank=True, choices=[('admin', 'admin'), ('country head', 'country head'), ('state head', 'state head'), ('city head', 'city head'), ('constitucy head', 'constitucy head'), ('ward head', 'ward head'), ('branch head', 'branch head'), ('member', 'member')], max_length=20, null=True)),
                ('occupation_type', models.CharField(blank=True, choices=[('business', 'business'), ('job', 'job')], max_length=20, null=True)),
                ('occupation_title', models.CharField(blank=True, max_length=255, null=True)),
                ('otp', models.CharField(blank=True, max_length=7, null=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('is_admin', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'account_user',
            },
        ),
        migrations.CreateModel(
            name='UserFamily',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('occupation_type', models.CharField(blank=True, choices=[('business', 'business'), ('job', 'job')], max_length=20, null=True)),
                ('occupation_title', models.CharField(blank=True, max_length=255, null=True)),
                ('aadhar', models.CharField(max_length=12, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]