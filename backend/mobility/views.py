import os
import json
from urllib.parse import quote
from django.conf import settings
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date, parse_time
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
import requests, secrets
import re
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import SiteContent, WebsiteSection, Vehicle, Testimonial, Booking, MediaAsset, BuilderSection, SiteTheme, CustomerProfile, Driver

CMS_MODELS = {
    'site-content': (SiteContent, 'Website Identity'),
    'sections': (WebsiteSection, 'Landing Page Sections'),
    'fleet': (Vehicle, 'Fleet & Pricing'),
    'bookings': (Booking, 'Ride Bookings'),
    'drivers': (Driver, 'Driver Management'),
    'testimonials': (Testimonial, 'Testimonials'),
    'media': (MediaAsset, 'Media Library'),
}

def staff_check(user):
    return user.is_authenticated and user.is_staff

def cms_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('cms_dashboard')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('cms_dashboard')
        error = 'Invalid staff username or password.'
    return render(request, 'cms_login.html', {'error': error})

def cms_logout(request):
    logout(request)
    return redirect('cms_login')

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_dashboard(request):
    return render(request, 'cms_dashboard.html', {
        'booking_count': Booking.objects.count(),
        'new_bookings': Booking.objects.filter(status='new').count(),
        'vehicle_count': Vehicle.objects.count(),
        'driver_count': Driver.objects.count(),
        'available_driver_count': Driver.objects.filter(is_active=True, status='available').count(),
        'section_count': WebsiteSection.objects.count(),
        'testimonial_count': Testimonial.objects.count(),
        'media_count': MediaAsset.objects.count(),
        'active_vehicle_count': Vehicle.objects.filter(is_active=True).count(),
        'recent_bookings': Booking.objects.order_by('-created_at')[:8],
    })

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_list(request, model_key):
    if model_key not in CMS_MODELS: raise Http404
    model, title = CMS_MODELS[model_key]
    return render(request, 'cms_list.html', {'title': title, 'model_key': model_key, 'objects': model.objects.all()})

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_create(request, model_key):
    return cms_form(request, model_key, None)

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_edit(request, model_key, pk):
    return cms_form(request, model_key, pk)

def cms_form(request, model_key, pk):
    if model_key not in CMS_MODELS: raise Http404
    model, title = CMS_MODELS[model_key]
    obj = get_object_or_404(model, pk=pk) if pk else None
    excluded = {'id', 'updated_at', 'created_at', 'uploaded_at'}
    fields = [f.name for f in model._meta.fields if f.name not in excluded]
    FormClass = type(f'{model.__name__}CMSForm', (forms.ModelForm,), {'Meta': type('Meta', (), {'model': model, 'fields': fields})})
    form = FormClass(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'{title} saved successfully.')
        return redirect('cms_list', model_key=model_key)
    return render(request, 'cms_form.html', {'form': form, 'title': title, 'model_key': model_key, 'is_edit': bool(obj)})

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_delete(request, model_key, pk):
    if model_key not in CMS_MODELS: raise Http404
    model, title = CMS_MODELS[model_key]
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, f'{title} item deleted.'); return redirect('cms_list', model_key=model_key)
    return render(request, 'cms_confirm_delete.html', {'object': obj, 'title': title, 'model_key': model_key})

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_booking_detail(request, pk):
    booking = get_object_or_404(Booking.objects.select_related('vehicle'), pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status', '')
        valid_statuses = {choice[0] for choice in Booking.STATUS}
        if status in valid_statuses:
            booking.status = status
            booking.save(update_fields=['status'])
            messages.success(request, f'Booking NTTS-{booking.pk:05d} status updated.')
            return redirect('cms_booking_detail', pk=booking.pk)
        messages.error(request, 'Please select a valid booking status.')
    return render(request, 'cms_booking_detail.html', {'booking': booking})


def track_booking(request):
    booking = None
    error = ''
    reference = request.POST.get('reference', '').strip() if request.method == 'POST' else request.GET.get('reference', '').strip()
    phone = request.POST.get('phone', '').strip() if request.method == 'POST' else ''
    if request.method == 'POST':
        digits = ''.join(ch for ch in reference if ch.isdigit())
        if not digits or not phone:
            error = 'Enter your booking reference and registered phone number.'
        else:
            booking = Booking.objects.select_related('vehicle').filter(pk=int(digits), phone=phone).first()
            if not booking:
                error = 'Booking not found. Check your reference and phone number.'
    status_steps = [
        ('new', 'Booking received', 'Your ride request has reached NTTS Mobility.'),
        ('accepted', 'Booking accepted', 'The team has confirmed your ride request.'),
        ('driver_assigned', 'Driver assigned', 'Your driver details can be shared by the NTTS team.'),
        ('ongoing', 'Ride in progress', 'Your journey is currently in progress.'),
        ('completed', 'Ride completed', 'Your trip has been marked as completed.'),
    ]
    current_index = next((i for i, item in enumerate(status_steps) if booking and item[0] == booking.status), -1)
    return render(request, 'track_booking.html', {
        'booking': booking, 'error': error, 'reference': reference,
        'status_steps': status_steps, 'current_status_index': current_index,
    })


@login_required(login_url='/customer/login/')
def my_rides(request):
    # My Rides belongs to customers. If an admin is signed in, show the
    # customer login screen instead of sending them back to the CMS dashboard.
    if request.user.is_staff:
        return redirect('customer_login')

    profile = get_object_or_404(
        CustomerProfile,
        user=request.user
    )

    bookings = (
        Booking.objects
        .filter(customer=profile)
        .select_related('vehicle')
        .order_by('-created_at')
    )

    return render(request, 'my_rides.html', {
        'profile': profile,
        'bookings': bookings,
    })

@login_required(login_url='/customer/login/')
def customer_profile(request):
    # Staff/admin accounts must never enter the customer portal.
    if request.user.is_staff:
        return redirect('cms_dashboard')
    profile = get_object_or_404(CustomerProfile, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('full_name','').strip()
        email = request.POST.get('email','').strip()
        if not name:
            messages.error(request, 'Please enter your name.')
        else:
            profile.full_name = name; profile.email = email; profile.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('customer_profile')
    return render(request, 'customer_profile.html', {'profile': profile})

def customer_logout(request):
    # This endpoint only logs out customer accounts; admins use /cms/logout/.
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('cms_dashboard')
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


def _customer_otp_cache_key(email):
    return "customer_email_otp:" + email.lower().strip()

def _customer_otp_cooldown_key(email):
    return "customer_email_otp_cooldown:" + email.lower().strip()

@require_http_methods(["GET", "POST"])
def customer_login(request):
    # My Rides must always show the customer login page, even if an admin
    # is currently signed in. A verified customer login will switch sessions.
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('my_rides')

    error = ""
    if request.method == "POST":
        action = request.POST.get("action", "send_otp")
        phone = re.sub(r"\D", "", request.POST.get("phone", ""))[-10:]
        email = request.POST.get("email", "").strip().lower()

        if not re.fullmatch(r"[6-9][0-9]{9}", phone):
            error = "Enter a valid 10-digit Indian mobile number."
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            error = "Enter a valid email address."
        elif action == "send_otp":
            if cache.get(_customer_otp_cooldown_key(email)):
                error = "Please wait 60 seconds before requesting another OTP."
            else:
                otp = f"{secrets.randbelow(1000000):06d}"
                subject = "Your NTTS Mobility login OTP"
                body = (
                    f"Your NTTS Mobility verification code is {otp}.\n\n"
                    "This code expires in 5 minutes. Do not share it with anyone."
                )
                try:
                    response = requests.post(
                        "https://api.brevo.com/v3/smtp/email",
                        headers={
                            "accept": "application/json",
                            "api-key": settings.BREVO_API_KEY,
                            "content-type": "application/json",
                        },
                        json={
                            "sender": {
                                "email": settings.DEFAULT_FROM_EMAIL,
                                "name": "NTTS Mobility",
                            },
                            "to": [{"email": email}],
                            "subject": subject,
                            "textContent": body,
                        },
                        timeout=15,
                    )

                    if response.status_code not in (200, 201, 202):
                        raise RuntimeError(
                            f"Brevo API error: {response.status_code} - {response.text[:300]}"
                        )

                    cache.set(_customer_otp_cache_key(email), {"otp": otp, "phone": phone}, timeout=300)
                    cache.set(_customer_otp_cooldown_key(email), True, timeout=60)
                    request.session["customer_otp_email"] = email
                    request.session["customer_otp_phone"] = phone
                    messages.success(request, "OTP sent to your email address. Please check your inbox and spam folder.")
                    return render(request, "customer_login.html", {"otp_sent": True, "email": email, "phone": phone})

                except Exception as exc:
                    print(f"Brevo OTP email error: {exc}")
                    error = "Unable to send OTP. Please check your verified sender email and Brevo API configuration."
        elif action == "verify_otp":
            entered_otp = request.POST.get("otp", "").strip()
            saved = cache.get(_customer_otp_cache_key(email))
            if (not saved or saved.get("phone") != phone or
                    not re.fullmatch(r"[0-9]{6}", entered_otp) or
                    not secrets.compare_digest(saved.get("otp", ""), entered_otp)):
                error = "Invalid or expired OTP. Please request a new OTP."
            else:
                user, _ = User.objects.get_or_create(username="customer_" + phone)
                if user.is_staff:
                    error = "This account is an administrator account. Please use the Admin Login page."
                else:
                    profile, _ = CustomerProfile.objects.get_or_create(
                        user=user,
                        defaults={"phone": phone, "email": email}
                    )
                    if profile.phone != phone:
                        profile.phone = phone
                    profile.email = email
                    profile.save(update_fields=["phone", "email"])

                    # Link only matching previous guest bookings to this verified customer.
                    guest_bookings = Booking.objects.filter(
                        customer__isnull=True,
                        email__iexact=email
                    )
                    for booking in guest_bookings:
                        booking_phone = re.sub(r"\D", "", booking.phone)[-10:]
                        if booking_phone == phone:
                            booking.customer = profile
                            booking.save(update_fields=["customer"])

                    cache.delete(_customer_otp_cache_key(email))
                    cache.delete(_customer_otp_cooldown_key(email))
                    request.session.pop("customer_otp_email", None)
                    request.session.pop("customer_otp_phone", None)
                    # If an admin is signed in in this browser, switch to the
                    # verified customer account instead of keeping the admin session.
                    if request.user.is_authenticated:
                        logout(request)
                    user.backend = "django.contrib.auth.backends.ModelBackend"
                    login(request, user)
                    return redirect("my_rides")

    return render(request, "customer_login.html", {
        "error": error,
        "otp_sent": bool(request.session.get("customer_otp_email")),
        "email": request.session.get("customer_otp_email", ""),
        "phone": request.session.get("customer_otp_phone", ""),
    })

def track_customer_ride(request, pk):
    if not request.user.is_authenticated:
        return redirect('customer_login')
    if request.user.is_staff:
        return redirect('cms_dashboard')
    profile = get_object_or_404(CustomerProfile, user=request.user)
    booking = get_object_or_404(Booking.objects.select_related('vehicle'), pk=pk, customer=profile)
    status_steps = [
        ('new','Booking received','Your ride request has reached NTTS Mobility.'),
        ('accepted','Booking accepted','The team has confirmed your ride request.'),
        ('driver_assigned','Driver assigned','Your driver details can be shared by the NTTS team.'),
        ('ongoing','Ride in progress','Your journey is currently in progress.'),
        ('completed','Ride completed','Your trip has been marked as completed.'),
    ]
    current_index = next((i for i,item in enumerate(status_steps) if item[0] == booking.status), -1)
    return render(request, 'track_customer_ride.html', {'booking':booking,'status_steps':status_steps,'current_status_index':current_index,'page_title':'Track Ride','page_heading':'Track Your Ride'})


def home(request):
    content = SiteContent.objects.filter(key='home').first()
    vehicles = Vehicle.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'home.html', {'content': content, 'vehicles': vehicles, 'testimonials': testimonials, 'cms_sections': WebsiteSection.objects.filter(is_visible=True), 'showcase_vehicles': Vehicle.objects.filter(is_active=True, showcase_enabled=True), 'builder_sections': BuilderSection.objects.filter(is_visible=True), 'site_theme': SiteTheme.objects.first()})

@require_POST
@csrf_protect
def create_booking(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        required = ['pickup', 'destination', 'passenger_name', 'phone']
        if any(not str(data.get(k, '')).strip() for k in required):
            return JsonResponse({'ok': False, 'message': 'Please complete all required fields.'}, status=400)
        phone = re.sub(r'[\s()+-]', '', str(data.get('phone', '')))
        if not re.fullmatch(r'(?:91)?[6-9]\d{9}', phone):
            return JsonResponse({'ok': False, 'message': 'Enter a valid 10-digit Indian mobile number (or +91 followed by 10 digits).'}, status=400)
        ride_date = parse_date(str(data.get('ride_date', '')).strip()) if data.get('ride_date') else None
        ride_time = parse_time(str(data.get('ride_time', '')).strip()) if data.get('ride_time') else None
        if data.get('ride_date') and not ride_date:
            return JsonResponse({'ok': False, 'message': 'Choose a valid ride date.'}, status=400)
        if ride_date and ride_date < timezone.localdate():
            return JsonResponse({'ok': False, 'message': 'Ride date cannot be in the past.'}, status=400)
        if data.get('ride_time') and not ride_time:
            return JsonResponse({'ok': False, 'message': 'Choose a valid ride time.'}, status=400)
        vehicle = Vehicle.objects.filter(pk=data.get('vehicle_id'), is_active=True).first() if data.get('vehicle_id') else None
        customer = CustomerProfile.objects.filter(user=request.user).first() if request.user.is_authenticated else None
        if customer and customer.phone != re.sub(r'[^0-9]', '', data['phone'])[-10:]:
            return JsonResponse({'ok': False, 'message': 'Please use your registered mobile number.'}, status=400)
        booking = Booking.objects.create(customer=customer, pickup=data['pickup'].strip(), destination=data['destination'].strip(), passenger_name=data['passenger_name'].strip(), phone=data['phone'].strip(), email=data.get('email', '').strip(), vehicle=vehicle, ride_date=ride_date, ride_time=ride_time)
        reference = f'NTTS-{booking.pk:05d}'
        vehicle_name = vehicle.name if vehicle else 'Not selected'
        ride_date = booking.ride_date.strftime('%d-%m-%Y') if booking.ride_date else 'Not specified'
        ride_time = booking.ride_time.strftime('%I:%M %p') if booking.ride_time else 'Depart Now'
        whatsapp_number = ''.join(ch for ch in getattr(settings, 'WHATSAPP_OWNER_NUMBER', '') if ch.isdigit())
        whatsapp_message = (
            f'New NTTS Mobility ride request\\n'
            f'Booking: {reference}\\n'
            f'Name: {booking.passenger_name}\\n'
            f'Phone: {booking.phone}\\n'
            f'Pickup: {booking.pickup}\\n'
            f'Destination: {booking.destination}\\n'
            f'Date: {ride_date}\\n'
            f'Time: {ride_time}\\n'
            f'Vehicle: {vehicle_name}'
        )
        whatsapp_url = f'https://wa.me/{whatsapp_number}?text={quote(whatsapp_message)}' if whatsapp_number else ''
        return JsonResponse({
            'ok': True,
            'message': f'Request received! Your booking reference is {reference}.',
            'reference': reference,
            'whatsapp_url': whatsapp_url,
        })
    except (ValueError, TypeError, KeyError):
        return JsonResponse({'ok': False, 'message': 'Invalid booking details.'}, status=400)


@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_builder(request):
    sections = BuilderSection.objects.all()
    theme = SiteTheme.objects.first() or SiteTheme.objects.create()
    return render(request, 'cms_builder.html', {'sections': sections, 'theme': theme})

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_builder_section(request, pk=None):
    obj = get_object_or_404(BuilderSection, pk=pk) if pk else None
    fields = ['title','eyebrow','body','image','layout','button_label','button_url','background_color','text_color','accent_color','is_visible','sort_order']
    FormClass = type('BuilderSectionForm', (forms.ModelForm,), {'Meta': type('Meta', (), {'model': BuilderSection, 'fields': fields})})
    form = FormClass(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Website section saved.'); return redirect('cms_builder')
    return render(request, 'cms_form.html', {'form': form, 'title': 'Visual Website Section', 'model_key': 'builder', 'is_edit': bool(obj)})

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
@require_POST
def cms_builder_delete(request, pk):
    get_object_or_404(BuilderSection, pk=pk).delete(); messages.success(request, 'Website section deleted.'); return redirect('cms_builder')

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
@require_POST
def cms_builder_reorder(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
        for index, section_id in enumerate(payload.get('order', [])):
            BuilderSection.objects.filter(pk=section_id).update(sort_order=index)
        return JsonResponse({'ok': True})
    except (ValueError, TypeError):
        return JsonResponse({'ok': False}, status=400)

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_theme(request):
    theme = SiteTheme.objects.first() or SiteTheme.objects.create()
    fields = ['primary_color','dark_color','background_color','heading_text_color','body_text_color','button_text_color','font_heading','font_body','border_radius']
    color_widgets = {name: forms.TextInput(attrs={'type': 'color', 'class': 'theme-color-input'}) for name in ['primary_color', 'dark_color', 'background_color', 'heading_text_color', 'body_text_color', 'button_text_color']}
    FormClass = type('SiteThemeForm', (forms.ModelForm,), {'Meta': type('Meta', (), {'model': SiteTheme, 'fields': fields, 'widgets': color_widgets})})
    form = FormClass(request.POST or None, instance=theme)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Global website design updated.'); return redirect('cms_theme')
    return render(request, 'cms_form.html', {'form': form, 'title': 'Global Website Design', 'model_key': 'theme', 'is_edit': True})

@login_required(login_url='/cms/login/')
@user_passes_test(staff_check, login_url='/cms/login/')
def cms_profile(request):
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if not user.check_password(request.POST.get('current_password', '')):
            messages.error(request, 'Current password is incorrect.')

        elif action == 'profile':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()

            if not all([first_name, email, username]):
                messages.error(request, 'Name, email and username are required.')
            elif User.objects.filter(username__iexact=username).exclude(pk=user.pk).exists():
                messages.error(request, 'This username is already taken.')
            elif User.objects.filter(email__iexact=email).exclude(pk=user.pk).exists():
                messages.error(request, 'This email is already in use.')
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()
                messages.success(request, 'Admin profile updated successfully.')
                return redirect('cms_profile')

        elif action == 'password':
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not new_password:
                messages.error(request, 'Enter a new password.')
            elif new_password != confirm_password:
                messages.error(request, 'New password and confirmation do not match.')
            else:
                try:
                    validate_password(new_password, user=user)
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password changed successfully.')
                    return redirect('cms_profile')
                except ValidationError as error:
                    for item in error.messages:
                        messages.error(request, item)

        else:
            messages.error(request, 'Invalid settings request.')

    return render(request, 'cms_profile.html', {'profile_user': user})
