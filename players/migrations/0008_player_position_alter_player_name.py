# Generated by Django 4.2.4 on 2024-03-21 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0007_alter_player_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(choices=[('Goalkeeper', 'Goalkeeper'), ('Right Back', 'Right Back'), ('Left Back', 'Left Back'), ('Center Back', 'Center Back'), ('Right Midfielder', 'Right Midfielder'), ('Central Midfielder', 'Central Midfielder'), ('Left Midfielder', 'Left Midfielder'), ('Attacking Midfielder', 'Attacking Midfielder'), ('Center Forward', 'Center Forward')], default='Unknown', max_length=50),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(default='Jennifer Henry', max_length=100),
        ),
    ]