from django.db import models

class SiteContent(models.Model):
    key = models.SlugField(unique=True, help_text='Use home for the homepage record')
    brand_name = models.CharField(max_length=80, default='NTTS MOBILITY')
    hero_eyebrow = models.CharField(max_length=100, default='NEXT-GEN URBAN TRANSIT')
    hero_title = models.CharField(max_length=180, default='Your Ride, Your Way — Anytime, Anywhere')
    hero_subtitle = models.TextField(default='Fast, safe, and sustainable rides at your fingertips.')
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#10844F')
    dark_color = models.CharField(max_length=7, default='#181C24')
    background_color = models.CharField(max_length=7, default='#FBFBF9')
    promo_text = models.CharField(max_length=200, default='Get ₹150 off your first 3 rides with code NTTSGO')
    footer_text = models.TextField(default='Moving cities forward with safer, smarter and greener mobility.')
    fleet_heading = models.CharField(max_length=160, default='Dynamic Fleet in Motion')
    fleet_subtitle = models.CharField(max_length=220, default='NTTS LIVE MOBILITY DECK')
    stats_one_value = models.CharField(max_length=30, default='10M+')
    stats_one_label = models.CharField(max_length=80, default='Rides Completed Safely')
    stats_two_value = models.CharField(max_length=30, default='4.9')
    stats_two_label = models.CharField(max_length=80, default='Avg Customer Satisfaction')
    stats_three_value = models.CharField(max_length=30, default='50+')
    stats_three_label = models.CharField(max_length=80, default='Metros & Cities Worldwide')
    stats_four_value = models.CharField(max_length=30, default='24/7')
    stats_four_label = models.CharField(max_length=80, default='Human Concierge & Safety')
    rides_heading = models.CharField(max_length=160, default='Choose Your Ride')
    rides_subtitle = models.CharField(max_length=240, default='Tailored transportation solutions calibrated for speed, comfort, or solo sprints.')
    process_heading = models.CharField(max_length=160, default='Ride in 3 Simple Steps')
    process_subtitle = models.TextField(default='From tapping your screen to stepping out at your destination—zero friction, all precision.')
    process_step_one_title = models.CharField(max_length=120, default='Enter Your Destination')
    process_step_one_body = models.TextField(default='Type in your pickup point or allow the geo-sensor to lock onto your precise spot automatically.')
    process_step_two_title = models.CharField(max_length=120, default='Choose Your Ride')
    process_step_two_body = models.TextField(default='Compare transparent upfront fares, precise vehicle models, and driver distance before locking in.')
    process_step_three_title = models.CharField(max_length=120, default='Sit Back & Relax')
    process_step_three_body = models.TextField(default='Track your driver, share ride details with loved ones, and pay cashlessly.')
    safety_heading = models.CharField(max_length=160, default='Your Safety is Our Priority')
    safety_subtitle = models.TextField(default='From algorithmic background vetting to emergency rapid-response teams on standby, our security infrastructure protects every kilometer.')
    pricing_heading = models.CharField(max_length=160, default='Simple, Transparent Pricing')
    pricing_subtitle = models.CharField(max_length=240, default='No hidden fuel fees. Upfront fares guaranteed before you confirm.')
    testimonials_heading = models.CharField(max_length=160, default='What Our Riders Say')
    testimonials_subtitle = models.TextField(default='Thousands of daily commuters rely on NTTS Mobility for punctual meetings, late-night flights, and stress-free city hops.')
    download_heading = models.CharField(max_length=160, default='Download NTTS Mobility Today')
    download_subtitle = models.TextField(default='Instant onboarding in 60 seconds.')
    carbon_badge_text = models.CharField(max_length=120, default='100% Carbon-Neutral Fleet Options')
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.key

class WebsiteSection(models.Model):
    """CMS-managed supplementary homepage content blocks."""
    SECTION_TYPES = [('text','Text'),('feature','Feature'),('announcement','Announcement')]
    title = models.CharField(max_length=160)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES, default='text')
    eyebrow = models.CharField(max_length=120, blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='sections/', blank=True, null=True)
    button_label = models.CharField(max_length=60, blank=True)
    button_url = models.CharField(max_length=300, blank=True)
    is_visible = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['sort_order', 'id']
    def __str__(self): return self.title

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=80, default='Sedan')
    description = models.TextField(blank=True)
    capacity = models.CharField(max_length=40, default='4 Passengers')
    base_fare = models.DecimalField(max_digits=9, decimal_places=2, default=80)
    per_km_fare = models.DecimalField(max_digits=8, decimal_places=2, default=14)
    eta = models.CharField(max_length=40, default='3m away')
    showcase_label = models.CharField(max_length=80, default='FIRST-CLASS CHAUFFEUR')
    luggage = models.CharField(max_length=60, default='2 Suitcases')
    privacy_tint = models.CharField(max_length=60, default='Grade A')
    rating = models.CharField(max_length=20, default='4.99')
    showcase_enabled = models.BooleanField(default=True, help_text='Show this vehicle in the animated Fleet carousel')
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['sort_order', 'id']
    def __str__(self): return self.name

class Booking(models.Model):
    customer = models.ForeignKey('CustomerProfile', on_delete=models.SET_NULL, blank=True, null=True, related_name='bookings')
    STATUS = [('new','New'),('accepted','Accepted'),('driver_assigned','Driver assigned'),('ongoing','Ongoing'),('completed','Completed'),('cancelled','Cancelled')]
    pickup = models.CharField(max_length=220)
    destination = models.CharField(max_length=220)
    ride_date = models.DateField(blank=True, null=True)
    ride_time = models.TimeField(blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, blank=True, null=True)
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, blank=True, null=True, related_name='bookings')
    passenger_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=25)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Ride #{self.pk} — {self.passenger_name}'

class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    role = models.CharField(max_length=120, blank=True)
    quote = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['sort_order', 'id']
    def __str__(self): return self.customer_name

class MediaAsset(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='library/')
    alt_text = models.CharField(max_length=180, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title


class BuilderSection(models.Model):
    """No-code, CMS-managed visual content block for the public website."""
    LAYOUTS = [('standard','Standard'),('split','Image + text'),('banner','Full-width banner'),('cards','Feature card')]
    title = models.CharField(max_length=160)
    eyebrow = models.CharField(max_length=120, blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='builder/', blank=True, null=True)
    layout = models.CharField(max_length=20, choices=LAYOUTS, default='standard')
    button_label = models.CharField(max_length=70, blank=True)
    button_url = models.CharField(max_length=300, blank=True)
    background_color = models.CharField(max_length=7, default='#FBFBF9')
    text_color = models.CharField(max_length=7, default='#181C24')
    accent_color = models.CharField(max_length=7, default='#10844F')
    is_visible = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['sort_order', 'id']
    def __str__(self): return self.title

class SiteTheme(models.Model):
    """Global visual theme editable without touching source code."""
    primary_color = models.CharField(max_length=7, default='#10844F')
    dark_color = models.CharField(max_length=7, default='#181C24')
    background_color = models.CharField(max_length=7, default='#FBFBF9')
    heading_text_color = models.CharField(max_length=7, default='#181C24')
    body_text_color = models.CharField(max_length=7, default='#475569')
    button_text_color = models.CharField(max_length=7, default='#FFFFFF')
    font_heading = models.CharField(max_length=80, default='Space Grotesk')
    font_body = models.CharField(max_length=80, default='Poppins')
    border_radius = models.PositiveSmallIntegerField(default=16)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return 'Global Website Theme'


class CustomerProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.phone


class Driver(models.Model):
    STATUS = [('available', 'Available'), ('on_trip', 'On Trip'), ('offline', 'Offline')]
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=25, unique=True)
    email = models.EmailField(blank=True)
    licence_number = models.CharField(max_length=80, unique=True)
    licence_expiry = models.DateField(blank=True, null=True)
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_drivers')
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='drivers/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} · {self.phone}'


class WebsiteBranding(models.Model):
    """Central identity and navigation labels used by the public website."""
    brand_name = models.CharField(max_length=100, default='NTTS MOBILITY')
    browser_title = models.CharField(max_length=160, default='NTTS MOBILITY | Your Ride, Your Way')
    tagline = models.CharField(max_length=200, blank=True, default='')
    logo = models.ImageField(upload_to='branding/', blank=True, null=True, help_text='Main logo used in the website header and footer')
    favicon = models.ImageField(upload_to='branding/', blank=True, null=True, help_text='Browser tab icon')
    header_home_label = models.CharField(max_length=50, default='Home')
    header_fleet_label = models.CharField(max_length=50, default='Fleet')
    header_process_label = models.CharField(max_length=50, default='How It Works')
    header_safety_label = models.CharField(max_length=50, default='Safety')
    header_pricing_label = models.CharField(max_length=50, default='Pricing')
    header_booking_label = models.CharField(max_length=60, default='Book a Ride')
    footer_company_name = models.CharField(max_length=120, default='NTTS Mobility Technologies')
    footer_company_heading = models.CharField(max_length=60, default='COMPANY')
    footer_support_heading = models.CharField(max_length=60, default='SUPPORT')
    footer_legal_heading = models.CharField(max_length=60, default='LEGAL')
    footer_about_label = models.CharField(max_length=60, default='About Us')
    footer_help_label = models.CharField(max_length=60, default='Help Center')
    footer_contact_label = models.CharField(max_length=60, default='Contact Concierge')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Website branding & names'
        verbose_name_plural = 'Website branding & names'

    def __str__(self):
        return self.brand_name


class PageContentItem(models.Model):
    """Editable cards/steps that belong to an individual public website page."""
    PAGE_CHOICES = [('home','Home Page'),('fleet','Fleet Page'),('process','How It Works Page'),('safety','Safety Page'),('pricing','Pricing Page'),('booking','Booking Page'),('testimonials','Testimonials Page'),('download','App Download Page'),('footer','Footer Page')]
    page = models.CharField(max_length=24, choices=PAGE_CHOICES, db_index=True)
    title = models.CharField(max_length=180)
    eyebrow = models.CharField(max_length=120, blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to='page-content/', blank=True, null=True)
    icon = models.CharField(max_length=80, blank=True, help_text='Optional icon name or short symbol')
    button_label = models.CharField(max_length=80, blank=True)
    button_url = models.CharField(max_length=300, blank=True)
    is_visible = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['page', 'sort_order', 'id']
        verbose_name = 'Page content item'
        verbose_name_plural = 'Page content items'
    def __str__(self):
        return f'{self.get_page_display()} — {self.title}'

# Proxy models create separate page-wise menus in the standard Django Admin.
class HomePageContent(SiteContent):
    class Meta: proxy = True; verbose_name = 'Home page'; verbose_name_plural = '01 · Home page'
class FleetPageContent(SiteContent):
    class Meta: proxy = True; verbose_name = 'Fleet page'; verbose_name_plural = '02 · Fleet page'
class ProcessPageContent(SiteContent):
    class Meta: proxy = True; verbose_name = 'How It Works page'; verbose_name_plural = '03 · How It Works page'
class SafetyPageContent(SiteContent):
    class Meta: proxy = True; verbose_name = 'Safety page'; verbose_name_plural = '04 · Safety page'
class PricingPageContent(SiteContent):
    class Meta: proxy = True; verbose_name = 'Pricing page'; verbose_name_plural = '05 · Pricing page'
class DownloadPageContent(SiteContent):
    class Meta: proxy = True; verbose_name = 'App download page'; verbose_name_plural = '06 · App download page'
class FooterPageContent(SiteContent):
    class Meta: proxy = True; verbose_name = 'Footer page'; verbose_name_plural = '07 · Footer page'
