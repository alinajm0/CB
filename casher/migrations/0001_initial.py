# Generated by Django 4.2b1 on 2023-02-21 15:30

import casher.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('img', models.ImageField(upload_to=casher.models.images_path)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('price', models.FloatField()),
                ('categoryID', models.OneToOneField(on_delete=models.SET('Coffee'), to='casher.category')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('count_of_product', models.IntegerField()),
                ('count_of_item', models.IntegerField()),
                ('total_price', models.FloatField()),
                ('discount', models.IntegerField()),
                ('price_after_discount', models.FloatField()),
                ('recipt_date', models.DateTimeField(auto_now_add=True)),
                ('customer_name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'Receipt',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('mail', models.EmailField(db_index=True, max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('isAdmin', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='receipt_item',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('product_date', models.DateTimeField(auto_now_add=True)),
                ('product_price', models.FloatField()),
                ('product_count', models.IntegerField()),
                ('product_id', models.OneToOneField(on_delete=models.SET('Deleted'), to='casher.product')),
                ('receipt_id', models.ForeignKey(on_delete=models.SET('Deleted'), to='casher.receipt')),
            ],
            options={
                'db_table': 'Receipt_item',
            },
        ),
    ]
