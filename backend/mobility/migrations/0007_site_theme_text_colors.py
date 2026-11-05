from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("mobility", "0006_driver_management")]
    operations = [
        migrations.AddField(model_name="sitetheme", name="heading_text_color", field=models.CharField(default="#181C24", max_length=7)),
        migrations.AddField(model_name="sitetheme", name="body_text_color", field=models.CharField(default="#475569", max_length=7)),
        migrations.AddField(model_name="sitetheme", name="button_text_color", field=models.CharField(default="#FFFFFF", max_length=7)),
    ]
