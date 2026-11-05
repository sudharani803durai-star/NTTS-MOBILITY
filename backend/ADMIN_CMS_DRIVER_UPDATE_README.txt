NTTS MOBILITY – CMS + Driver Management update
================================================

Included changes
- Added Driver model with name, phone, email, licence number/expiry, assigned vehicle, availability, active flag, photo and notes.
- Added optional driver assignment to each Booking.
- Added /cms/drivers/ management through the existing CMS generic list/form workflow.
- Added Driver to Django admin.
- Added shared CMS styling stylesheet and linked it to the CMS templates.
- Existing WebsiteSection, BuilderSection, SiteContent, SiteTheme, Vehicle, Testimonial and MediaAsset content tools are retained.

Important scope note
The existing project already supports editing many homepage content fields through Homepage Content, Page Sections and Website Builder. Some navigation labels, fixed booking-form labels, and parts of the public-page structure remain hard-coded in templates; this ZIP does not claim those are all editable yet. A full page-by-page content schema and preview/publish workflow is a separate next implementation stage.

Install/update
1. Back up your current project and database.
2. Replace the project files with this package (do not overwrite your own .env).
3. Open PowerShell in backend folder and activate your existing virtual environment.
4. Run:
   python manage.py makemigrations mobility
   python manage.py migrate
   python manage.py check
   python manage.py runserver
5. Open http://127.0.0.1:8000/cms/ and login with your existing staff account.
6. Open Drivers from the CMS dashboard. Add a driver, save, then edit a booking and select the driver.

Security
- .env and Firebase service-account private key are intentionally excluded.
- Keep your own .env locally and never upload it publicly.
- Rotate any SMTP credentials previously shared in chat.
- Do not commit private keys or credentials to Git.
