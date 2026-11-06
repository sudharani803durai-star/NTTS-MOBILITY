from django.db import migrations, models

def create_default_branding(apps, schema_editor):
    Branding = apps.get_model('mobility', 'WebsiteBranding')
    Branding.objects.using(schema_editor.connection.alias).get_or_create(pk=1)

class Migration(migrations.Migration):
    dependencies = [('mobility', '0007_site_theme_text_colors')]
    operations = [migrations.CreateModel(name='WebsiteBranding', fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('brand_name', models.CharField(default='NTTS MOBILITY', max_length=100)),
        ('browser_title', models.CharField(default='NTTS MOBILITY | Your Ride, Your Way', max_length=160)),
        ('tagline', models.CharField(blank=True, default='', max_length=200)),
        ('logo', models.ImageField(blank=True, help_text='Main logo used in the website header and footer', null=True, upload_to='branding/')),
        ('favicon', models.ImageField(blank=True, help_text='Browser tab icon', null=True, upload_to='branding/')),
        ('header_home_label', models.CharField(default='Home', max_length=50)),
        ('header_fleet_label', models.CharField(default='Fleet', max_length=50)),
        ('header_process_label', models.CharField(default='How It Works', max_length=50)),
        ('header_safety_label', models.CharField(default='Safety', max_length=50)),
        ('header_pricing_label', models.CharField(default='Pricing', max_length=50)),
        ('header_booking_label', models.CharField(default='Book a Ride', max_length=60)),
        ('footer_company_name', models.CharField(default='NTTS Mobility Technologies', max_length=120)),
        ('footer_company_heading', models.CharField(default='COMPANY', max_length=60)),
        ('footer_support_heading', models.CharField(default='SUPPORT', max_length=60)),
        ('footer_legal_heading', models.CharField(default='LEGAL', max_length=60)),
        ('footer_about_label', models.CharField(default='About Us', max_length=60)),
        ('footer_help_label', models.CharField(default='Help Center', max_length=60)),
        ('footer_contact_label', models.CharField(default='Contact Concierge', max_length=60)),
        ('updated_at', models.DateTimeField(auto_now=True)),
    ]), migrations.RunPython(create_default_branding, migrations.RunPython.noop)]
