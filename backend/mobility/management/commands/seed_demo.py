from django.core.management.base import BaseCommand
from mobility.models import SiteContent, Vehicle, Testimonial

class Command(BaseCommand):
    help = "Create editable starter content for NTTS Mobility"
    def handle(self, *args, **kwargs):
        SiteContent.objects.get_or_create(key="home")
        samples = [
            ("Compact Sedan","Daily commute","Affordable daily commutes with reliable drivers and quiet air-conditioned cabins.", "4 Seats",80,14,"3m away"),
            ("Executive Sedan","Executive","Luxury executive travel with premium amenities and professional chauffeurs.", "4 Seats",140,18,"5m away"),
            ("NTTS Luxe EV","Electric","Zero-emission electric sedans with a whisper-quiet cabin.", "4 Seats",200,24,"2m away"),
            ("Spacious SUV","Family & Group","Expansive cabin engineered for group trips and airport travel.", "6–7 Seats",260,28,"6m away"),
        ]
        for i, (name,cat,desc,cap,base,km,eta) in enumerate(samples):
            Vehicle.objects.get_or_create(name=name, defaults={"category":cat,"description":desc,"capacity":cap,"base_fare":base,"per_km_fare":km,"eta":eta,"is_featured":i==2,"sort_order":i})
        reviews = [
            ("Priya Sharma","Daily Tech Commuter","The punctuality and EV silence make all the difference. NTTS Mobility is now our preferred ride.",5),
            ("Marcus Vance","Executive Rider","Impeccable electric sedans, a quiet cabin and professional chauffeurs.",5),
            ("Dr. Ananya Roy","Night Physician","The driver checks and safety features give me peace of mind.",5),
        ]
        for i,(name,role,quote,rating) in enumerate(reviews):
            Testimonial.objects.get_or_create(customer_name=name, defaults={"role":role,"quote":quote,"rating":rating,"sort_order":i})
        self.stdout.write(self.style.SUCCESS("Demo content created. Manage it anytime in /cms/login/."))
