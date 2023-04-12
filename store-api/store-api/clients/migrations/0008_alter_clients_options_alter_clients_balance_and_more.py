# Generated by Django 4.0 on 2023-04-10 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_alter_clients_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clients',
            options={'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterField(
            model_name='clients',
            name='balance',
            field=models.PositiveIntegerField(default=0, verbose_name='Balance'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='password',
            field=models.CharField(max_length=255, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='status',
            field=models.CharField(choices=[('default', 'DEFAULT'), ('premium', 'PREMIUM')], default='default', max_length=255, verbose_name='Status'),
        ),
    ]