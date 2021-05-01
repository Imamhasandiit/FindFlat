# Generated by Django 3.0.5 on 2020-04-23 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=250)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/%Y/%m/%d/')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=250)),
                ('status', models.CharField(choices=[('0', 'Rent'), ('1', 'Sale')], max_length=10)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('area', models.CharField(max_length=200)),
                ('rooms', models.CharField(choices=[('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'), ('5', 'Five'), ('6', 'FIx')], max_length=10)),
                ('wash_rooms', models.CharField(choices=[('1', 'One'), ('2', 'Two'), ('3', 'Three')], max_length=10)),
                ('city', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
                ('booked', models.BooleanField(default=False)),
                ('start_time', models.DateField()),
                ('end_time', models.DateField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_listings', to='listings.Category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_listings', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/%Y/%m/%d/')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_images', to='listings.Listing')),
            ],
        ),
        migrations.CreateModel(
            name='ListingExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('0', 'No'), ('1', 'Yes')], max_length=10)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_extras', to='listings.Listing')),
            ],
        ),
    ]