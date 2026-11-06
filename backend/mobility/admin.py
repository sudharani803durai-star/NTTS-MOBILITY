from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteContent, WebsiteSection, Vehicle, Booking, Testimonial, MediaAsset,
    BuilderSection, SiteTheme, Driver, CustomerProfile, WebsiteBranding,
    PageContentItem, HomePageContent, FleetPageContent, ProcessPageContent, SafetyPageContent, PricingPageContent, DownloadPageContent, FooterPageContent,
)

admin.site.site_header = 'NTTS MOBILITY — Website & Operations Admin'
admin.site.site_title = 'NTTS MOBILITY Admin'
admin.site.index_title = 'Manage website content, images, customers and ride bookings'
admin.site.site_url = '/'


def image_preview(obj, field_name, width=150):
    image = getattr(obj, field_name, None)
    if image and getattr(image, 'url', None):
        return format_html('<a href="{}" target="_blank"><img src="{}" style="max-width:{}px;max-height:110px;object-fit:contain;border:1px solid #ddd;border-radius:8px;padding:3px;background:#fff"></a>', image.url, image.url, width)
    return 'No image uploaded'


class PageContentAdmin(admin.ModelAdmin):
    """One existing home record, presented as separate page editors."""
    list_display = ('key', 'brand_name', 'updated_at')
    readonly_fields = ('updated_at', 'hero_image_preview')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not qs.filter(key='home').exists():
            SiteContent.objects.get_or_create(key='home')
        return qs.filter(key='home')
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    @admin.display(description='Current hero image')
    def hero_image_preview(self, obj): return image_preview(obj, 'hero_image', 220)

@admin.register(HomePageContent)
class HomePageAdmin(PageContentAdmin):
    fieldsets = (('Home page identity', {'fields': ('key','brand_name','hero_eyebrow','hero_title','hero_subtitle','hero_image','hero_image_preview')}), ('Promotional banner', {'fields': ('promo_text',)}), ('Homepage statistics', {'fields': ('stats_one_value','stats_one_label','stats_two_value','stats_two_label','stats_three_value','stats_three_label','stats_four_value','stats_four_label')}), ('Footer introduction', {'fields': ('footer_text', 'updated_at')}))
@admin.register(FleetPageContent)
class FleetPageAdmin(PageContentAdmin):
    fieldsets = (('Fleet showcase headings', {'fields': ('fleet_heading','fleet_subtitle','rides_heading','rides_subtitle','carbon_badge_text','updated_at')}),)
@admin.register(ProcessPageContent)
class ProcessPageAdmin(PageContentAdmin):
    fieldsets = (('How It Works heading', {'fields': ('process_heading','process_subtitle')}), ('Step 01', {'fields': ('process_step_one_title','process_step_one_body')}), ('Step 02', {'fields': ('process_step_two_title','process_step_two_body')}), ('Step 03', {'fields': ('process_step_three_title','process_step_three_body','updated_at')}))
@admin.register(SafetyPageContent)
class SafetyPageAdmin(PageContentAdmin):
    fieldsets = (('Safety page content', {'fields': ('safety_heading','safety_subtitle','updated_at')}),)
@admin.register(PricingPageContent)
class PricingPageAdmin(PageContentAdmin):
    fieldsets = (('Pricing page content', {'fields': ('pricing_heading','pricing_subtitle','updated_at')}),)
@admin.register(DownloadPageContent)
class DownloadPageAdmin(PageContentAdmin):
    fieldsets = (('App download content', {'fields': ('download_heading','download_subtitle','promo_text','updated_at')}),)
@admin.register(FooterPageContent)
class FooterPageAdmin(PageContentAdmin):
    fieldsets = (('Footer content', {'fields': ('footer_text','brand_name','updated_at')}),)

@admin.register(PageContentItem)
class PageContentItemAdmin(admin.ModelAdmin):
    list_display = ('page','title','image_preview','is_visible','sort_order','updated_at')
    list_filter = ('page','is_visible')
    search_fields = ('title','eyebrow','body')
    list_editable = ('is_visible','sort_order')
    readonly_fields = ('updated_at','image_preview')
    fieldsets = (('Choose page and content', {'fields': ('page','title','eyebrow','body','icon','image','image_preview')}), ('Optional button', {'fields': ('button_label','button_url')}), ('Display settings', {'fields': ('is_visible','sort_order','updated_at')}))
    @admin.display(description='Image preview')
    def image_preview(self,obj): return image_preview(obj,'image',110)

@admin.register(SiteTheme)
class SiteThemeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'primary_color', 'font_heading', 'font_body', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(WebsiteSection)
class WebsiteSectionAdmin(admin.ModelAdmin):
    list_display = ('title','section_type','image_preview','is_visible','sort_order','updated_at')
    list_filter = ('section_type','is_visible')
    search_fields = ('title','eyebrow','body')
    list_editable = ('is_visible','sort_order')
    readonly_fields = ('updated_at','image_preview')
    save_as = True
    fieldsets = (
        ('Section content', {'fields': ('title','section_type','eyebrow','body','button_label','button_url')}),
        ('Section image', {'fields': ('image','image_preview')}),
        ('Display settings', {'fields': ('is_visible','sort_order','updated_at')}),
    )

    @admin.display(description='Image')
    def image_preview(self, obj):
        return image_preview(obj, 'image', 110)


@admin.register(BuilderSection)
class BuilderSectionAdmin(admin.ModelAdmin):
    list_display = ('title','layout','image_preview','is_visible','sort_order','updated_at')
    list_filter = ('layout','is_visible')
    search_fields = ('title','eyebrow','body')
    list_editable = ('is_visible','sort_order')
    readonly_fields = ('updated_at','image_preview')
    save_as = True
    fieldsets = (
        ('Section content', {'fields': ('title','eyebrow','body','layout','button_label','button_url')}),
        ('Section image', {'fields': ('image','image_preview')}),
        ('Section design', {'fields': ('background_color','text_color','accent_color')}),
        ('Publish on website', {'fields': ('is_visible','sort_order','updated_at')}),
    )

    @admin.display(description='Image preview')
    def image_preview(self, obj):
        return image_preview(obj, 'image', 110)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name','category','image_preview','base_fare','per_km_fare','is_active','is_featured','showcase_enabled','sort_order')
    list_filter = ('category','is_active','is_featured','showcase_enabled')
    search_fields = ('name','description')
    list_editable = ('base_fare','per_km_fare','is_active','is_featured','showcase_enabled','sort_order')
    readonly_fields = ('image_preview',)

    @admin.display(description='Vehicle image')
    def image_preview(self, obj):
        return image_preview(obj, 'image', 110)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','passenger_name','phone','email','pickup','destination','ride_date','ride_time','vehicle','driver','status','created_at')
    list_filter = ('status','ride_date','created_at','vehicle')
    search_fields = ('passenger_name','phone','email','pickup','destination','customer__full_name','customer__phone')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 30
    fieldsets = (
        ('Customer details', {'fields': ('customer','passenger_name','phone','email')}),
        ('Ride details', {'fields': ('pickup','destination','ride_date','ride_time','vehicle')}),
        ('Operations', {'fields': ('driver','status','created_at')}),
    )


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone','licence_number','assigned_vehicle','status','is_active')
    list_filter = ('status','is_active')
    search_fields = ('full_name','phone','email','licence_number')
    list_editable = ('status','is_active')
    readonly_fields = ('created_at','updated_at','photo_preview')

    @admin.display(description='Driver photo')
    def photo_preview(self, obj):
        return image_preview(obj, 'photo', 110)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name','role','photo_preview','rating','is_active','sort_order')
    list_filter = ('is_active','rating')
    list_editable = ('rating','is_active','sort_order')
    search_fields = ('customer_name','quote')
    readonly_fields = ('photo_preview',)

    @admin.display(description='Photo')
    def photo_preview(self, obj):
        return image_preview(obj, 'photo', 90)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('title','image_preview','alt_text','uploaded_at')
    search_fields = ('title','alt_text')
    readonly_fields = ('uploaded_at','image_preview')

    @admin.display(description='Image')
    def image_preview(self, obj):
        return image_preview(obj, 'image', 110)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone','email','created_at')
    search_fields = ('full_name','phone','email')
    readonly_fields = ('created_at',)


@admin.register(WebsiteBranding)
class WebsiteBrandingAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'browser_title', 'updated_at')
    readonly_fields = ('updated_at', 'logo_preview', 'favicon_preview')
    fieldsets = (
        ('Brand identity', {'fields': ('brand_name', 'browser_title', 'tagline', 'logo', 'logo_preview', 'favicon', 'favicon_preview')}),
        ('Header / Navbar names', {'fields': ('header_home_label', 'header_fleet_label', 'header_process_label', 'header_safety_label', 'header_pricing_label', 'header_booking_label')}),
        ('Footer names', {'fields': ('footer_company_name', 'footer_company_heading', 'footer_support_heading', 'footer_legal_heading', 'footer_about_label', 'footer_help_label', 'footer_contact_label')}),
        ('Record information', {'fields': ('updated_at',)}),
    )

    @admin.display(description='Current logo')
    def logo_preview(self, obj):
        return image_preview(obj, 'logo', 220)

    @admin.display(description='Current favicon')
    def favicon_preview(self, obj):
        return image_preview(obj, 'favicon', 80)
