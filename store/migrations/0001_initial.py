# Generated by Django 3.2 on 2024-05-25 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TshirtProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('slug', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('tshirtproperty_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.tshirtproperty')),
            ],
            bases=('store.tshirtproperty',),
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('tshirtproperty_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.tshirtproperty')),
            ],
            bases=('store.tshirtproperty',),
        ),
        migrations.CreateModel(
            name='IdealFor',
            fields=[
                ('tshirtproperty_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.tshirtproperty')),
            ],
            bases=('store.tshirtproperty',),
        ),
        migrations.CreateModel(
            name='NeckType',
            fields=[
                ('tshirtproperty_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.tshirtproperty')),
            ],
            bases=('store.tshirtproperty',),
        ),
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('tshirtproperty_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.tshirtproperty')),
            ],
            bases=('store.tshirtproperty',),
        ),
        migrations.CreateModel(
            name='Sleeve',
            fields=[
                ('tshirtproperty_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.tshirtproperty')),
            ],
            bases=('store.tshirtproperty',),
        ),
        migrations.CreateModel(
            name='Tshirt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500, null=True)),
                ('discount', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='upload/images/')),
                ('Occasion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.occasion')),
                ('Sleeve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.sleeve')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.brand')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.color')),
                ('ideal_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.idealfor')),
                ('neck_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.necktype')),
            ],
            options={
                'db_table': 'table_tshirt',
            },
        ),
    ]
