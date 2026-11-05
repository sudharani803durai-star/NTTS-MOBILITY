from django.contrib import admin
from .models import SiteContent, WebsiteSection, Vehicle, Booking, Testimonial, MediaAsset, Driver

admin.site.site_header = 'NTTS MOBILITY — Content Management'
admin.site.site_title = 'NTTS MOBILITY CMS'
admin.site.index_title = 'Manage your website and ride operations'
admin.site.site_url = '/cms/'

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'brand_name', 'updated_at')
    fieldsets = (
        ('Website identity & theme', {'fields': ('key','brand_name','primary_color','dark_color','background_color')}),
        ('Hero content', {'fields': ('hero_eyebrow','hero_title','hero_subtitle','hero_image')}),
        ('Promotion & footer', {'fields': ('promo_text','footer_text')}),
    )

@admin.register(WebsiteSection)
class WebsiteSectionAdmin(admin.ModelAdmin):
    list_display = ('title','section_type','is_visible','sort_order','updated_at')
    list_filter = ('section_type','is_visible')
    search_fields = ('title','eyebrow','body')
    list_editable = ('is_visible','sort_order')
    fieldsets = (
        ('Section content', {'fields': ('title','section_type','eyebrow','body','image')}),
        ('Call to action', {'fields': ('button_label','button_url')}),
        ('Display controls', {'fields': ('is_visible','sort_order')}),
    )

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name','category','base_fare','per_km_fare','is_active','sort_order')
    list_filter = ('category','is_active','is_featured')
    search_fields = ('name','description')
    list_editable = ('base_fare','per_km_fare','is_active','sort_order')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','passenger_name','pickup','destination','vehicle','status','created_at')
    list_filter = ('status','created_at')
    search_fields = ('passenger_name','phone','pickup','destination')
    readonly_fields = ('created_at',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name','role','rating','is_active','sort_order')
    list_editable = ('rating','is_active','sort_order')
    search_fields = ('customer_name','quote')

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('title','alt_text','uploaded_at')
    search_fields = ('title','alt_text')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'licence_number', 'assigned_vehicle', 'status', 'is_active')
    list_filter = ('status', 'is_active')
    search_fields = ('full_name', 'phone', 'email', 'licence_number')
    list_editable = ('status', 'is_active')
