from django.db import migrations, models

def seed_existing_items(apps, schema_editor):
    Item = apps.get_model('mobility', 'SectionItem')
    db = schema_editor.connection.alias
    process = [
        ('STEP 01', 'Enter Your Destination', 'Type in your pickup point or allow the geo-sensor to lock onto your precise spot automatically.', 'Instant GPS coordinate detection', '⌖'),
        ('STEP 02', 'Choose Your Ride', 'Compare transparent upfront fares, precise vehicle models, and driver distance before locking in.', 'Locked fixed price — no surprises', '☷'),
        ('STEP 03', 'Sit Back & Relax', "Track your driver's real-time trajectory, share ride details with loved ones, and pay cashlessly.", 'Encrypted telemetry & live track', '✓'),
    ]
    safety = [
        ('', 'Verified Drivers', 'Multi-point background and driving record screening before first dispatch.', '', '▣'),
        ('', 'Live GPS Tracking', 'Share live telemetry links with contacts so they see your precise spot in real-time.', '', '⌖'),
        ('', 'SOS Emergency Button', 'Direct one-tap pipeline to emergency support and 24/7 internal dispatch.', '', '+'),
        ('', 'Masked Numbers', 'In-app calling keeps your personal number private.', '', '▯'),
        ('', '2-Way Accountability', 'Mutual rating ensures riders and drivers uphold high standards.', '', '⇄'),
        ('', 'Accident Cover', 'Added protection for every booked ride.', '', '✓'),
    ]
    for section, rows in [('process', process), ('safety', safety)]:
        if not Item.objects.using(db).filter(section=section).exists():
            for i, (eyebrow, title, body, detail, icon) in enumerate(rows, 1):
                Item.objects.using(db).create(section=section, eyebrow=eyebrow, title=title, body=body, detail=detail, icon_text=icon, sort_order=i)

class Migration(migrations.Migration):
    dependencies = [('mobility', '0008_website_branding')]
    operations = [
        migrations.CreateModel(name='SectionItem', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('section', models.CharField(choices=[('process', 'How It Works'), ('safety', 'Safety')], max_length=24)),
            ('eyebrow', models.CharField(blank=True, max_length=80)),
            ('title', models.CharField(max_length=160)),
            ('body', models.TextField(blank=True)),
            ('detail', models.CharField(blank=True, max_length=220)),
            ('icon_text', models.CharField(blank=True, default='•', max_length=12)),
            ('sort_order', models.PositiveIntegerField(default=0)),
            ('is_visible', models.BooleanField(default=True)),
        ], options={'ordering': ['section', 'sort_order', 'id'], 'verbose_name': 'Section content item', 'verbose_name_plural': 'Section content items'}),
        migrations.RunPython(seed_existing_items, migrations.RunPython.noop),
    ]
