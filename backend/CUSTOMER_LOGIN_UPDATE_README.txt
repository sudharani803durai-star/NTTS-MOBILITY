NTTS MOBILITY CUSTOMER ACCOUNT UPDATE
======================================

Included:
- Customer mobile number OTP request and OTP verification views using MSG91 API.
- Customer account/profile model and profile editing page.
- Authenticated My Rides dashboard.
- Per-booking Track This Ride page, restricted to the signed-in customer.
- Navbar links for My Rides, Login/Profile and Logout.
- Readability-focused typography updates.
- Existing separate staff CMS login remains in place.

IMPORTANT SETUP
1. Back up your existing database and project.
2. Install requirements: pip install -r requirements.txt
3. Copy .env.example to .env if you do not already have one.
4. Set MSG91_AUTH_KEY and MSG91_TEMPLATE_ID in backend/.env.
5. Ensure the MSG91 OTP template is approved and your account can send OTPs.
6. Run:
   python manage.py makemigrations mobility
   python manage.py migrate
7. Restart the Django server.

Limitations / required verification:
- MSG91 credentials, OTP template, KYC/DLT, account permissions and live SMS delivery were not available for testing.
- Existing bookings created before this update are not automatically linked to customer profiles.
- New bookings are attached to the logged-in customer only when the customer is signed in at booking time.
- The current website CMS builder still edits its supported content blocks/theme; it is not yet a complete page-by-page visual editor for every hardcoded component or every CMS logo/navigation element.
- Run full Django/MySQL and browser testing before deploying.
