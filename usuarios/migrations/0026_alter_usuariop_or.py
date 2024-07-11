# Generated by Django 4.2.6 on 2024-07-11 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0025_remove_area_abrevarea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariop',
            name='OR',
            field=models.CharField(choices=[('1', 'OR AGS'), ('2', 'OR BC'), ('3', 'OR BCS'), ('4', 'OR CAMP'), ('5', 'OR COAH'), ('6', 'OR COL'), ('7', 'OR CHIS'), ('8', 'OR CHIH'), ('9', 'OR CDMX'), ('10', 'OR DGO'), ('11', 'OR GTO'), ('12', 'OR GRO'), ('13', 'OR HGO'), ('14', 'OR JAL'), ('15', 'OR EDOMEX'), ('16', 'OR MICH'), ('17', 'OR MOR'), ('18', 'OR NAY'), ('19', 'OR NL'), ('20', 'OR OAX'), ('21', 'OR PUE'), ('22', 'OR QRO'), ('23', 'OR QROO'), ('24', 'OR SLP'), ('25', 'OR SIN'), ('26', 'OR SON'), ('27', 'OR TAB'), ('28', 'OR TAMPS'), ('29', 'OR TLX'), ('30', 'OR VER'), ('31', 'OR YUC'), ('32', 'OR ZAC'), ('33', 'DGTIC'), ('34', 'DGCM'), ('35', 'DGRAM'), ('36', 'DG'), ('37', 'SCJ'), ('38', 'DGA'), ('39', 'DGECCC'), ('40', 'DGCOR')], default='9', max_length=2),
        ),
    ]
