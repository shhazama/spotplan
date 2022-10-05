# Generated by Django 3.2 on 2022-10-02 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spotplan', '0004_auto_20220929_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(choices=[('j1', '北海道'), ('j2', '青森県'), ('j3', '岩手県'), ('j4', '宮城県'), ('j5', '秋田県'), ('j6', '山形県'), ('j7', '福島県'), ('j8', '茨城県'), ('j9', '栃木県'), ('j10', '群馬県'), ('j11', '埼玉県'), ('j12', '千葉県'), ('j13', '東京都'), ('j14', '神奈川県'), ('j15', '新潟県'), ('j16', '富山県'), ('j17', '石川県'), ('j18', '福井県'), ('j19', '山梨県'), ('j20', '長野県'), ('j21', '岐阜県'), ('j22', '静岡県'), ('j23', '愛知県'), ('j24', '三重県'), ('j25', '滋賀県'), ('j26', '京都府'), ('j27', '大阪府'), ('j28', '兵庫県'), ('j29', '奈良県'), ('j30', '和歌山県'), ('j31', '鳥取県'), ('j32', '島根県'), ('j33', '岡山県'), ('j34', '広島県'), ('j35', '山口県'), ('j36', '徳島県'), ('j37', '香川県'), ('j38', '愛媛県'), ('j39', '高知県'), ('j40', '福岡県'), ('j41', '佐賀県'), ('j42', '長崎県'), ('j43', '熊本県'), ('j44', '大分県'), ('j45', '宮崎県'), ('j46', '鹿児島県'), ('j47', '沖縄県')], max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='city',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='spotplan.city'),
        ),
    ]