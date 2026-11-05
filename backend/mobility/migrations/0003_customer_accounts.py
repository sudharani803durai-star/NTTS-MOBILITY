from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('mobility', '0002_full_site_cms_and_fleet_showcase'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=120)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='mobility.customerprofile'),
        ),
    ]
