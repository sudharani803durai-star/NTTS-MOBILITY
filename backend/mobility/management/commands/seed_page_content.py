from django.core.management.base import BaseCommand
from mobility.models import SiteContent, PageContentItem

class Command(BaseCommand):
    help = "Create the existing NTTS Mobility page content in Django Admin, without duplicating records."
    def handle(self, *args, **options):
        SiteContent.objects.get_or_create(key="home")
        process = [
            ("Enter Your Destination", "Type in your pickup point or allow the geo-sensor to lock onto your precise spot automatically.", "STEP 01", "⌖"),
            ("Choose Your Ride", "Compare transparent upfront fares, precise vehicle models, and driver distance before locking in.", "STEP 02", "☷"),
            ("Sit Back & Relax", "Track your driver's real-time trajectory, share ride details with loved ones, and pay cashlessly.", "STEP 03", "✓"),
        ]
        safety = [
            ("Verified Drivers", "Multi-point background and driving record screening before first dispatch.", "✓"),
            ("Live GPS Tracking", "Share live telemetry links with contacts so they see your precise spot in real-time.", "⌖"),
            ("SOS Emergency Button", "Direct one-tap pipeline to emergency support and 24/7 internal dispatch.", "＋"),
            ("Masked Numbers", "In-app calling keeps your personal number private.", "▣"),
            ("2-Way Accountability", "Mutual rating ensures riders and drivers uphold high standards.", "⇄"),
            ("Accident Cover", "Added protection for every booked ride.", "✓"),
        ]
        for i,(title,body,eyebrow,icon) in enumerate(process,1):
            PageContentItem.objects.get_or_create(page="process", title=title, defaults={"body":body,"eyebrow":eyebrow,"icon":icon,"sort_order":i})
        for i,(title,body,icon) in enumerate(safety,1):
            PageContentItem.objects.get_or_create(page="safety", title=title, defaults={"body":body,"icon":icon,"sort_order":i})
        self.stdout.write(self.style.SUCCESS("Existing Home record and How It Works / Safety cards are available in Django Admin. Existing edits were preserved."))
