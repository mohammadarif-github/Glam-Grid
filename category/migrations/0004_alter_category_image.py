# Generated by Django 5.0.1 on 2024-05-09 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_maincategory_category_maincategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='media/category'),
        ),
    ]
