# Generated by Django 3.2 on 2022-09-29 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spotplan', '0002_alter_place_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(choices=[('hokkaido', '北海道地方'), ('touhoku', '東北地方'), ('kannto', '関東地方'), ('tyubu', '中部地方'), ('kinki', '近畿地方'), ('tyugoku', '中国地方'), ('shikoku', '四国地方'), ('kyusyu', '九州地方')], max_length=100)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotplan.place')),
            ],
        ),
    ]
