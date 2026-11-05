# NTTS MOBILITY — Figma-led Django CMS project

## What is included
- Django website with the supplied NTTS logo and reference imagery already included.
- Custom CMS at `/cms/login/` (not Django Admin).
- Website Identity & Hero: edit hero text, brand colours, section headings/copy, statistics, promo and footer.
- All Website Sections: add/edit/delete extra content blocks, upload images, set visibility and display order.
- Fleet & Pricing: add/edit/delete vehicles, upload a separate car photo for each vehicle, set price/capacity/specifications, enable/disable fleet carousel visibility and reorder vehicles.
- Animated fleet carousel: category tabs, previous/next arrows and dots switch vehicle name, description, image and specifications.
- Bookings, testimonials and media library management.
- Responsive hover, reveal, transition and motion effects with reduced-motion accessibility support.

## Important image note
The supplied ZIP contains the NTTS logo, the Figma SUV illustration and screenshots of reference sections, but it does not contain a separate set of original vehicle photography for every car. The Fleet CMS therefore supports uploading a real photo for each vehicle. Until a photo is uploaded, the showcase uses the supplied Figma SUV image as a fallback. Upload transparent-background or clean side-profile car photos for the best result.

## Setup (Windows PowerShell)
1. Extract this ZIP. Open PowerShell in `ntts_work\backend`.
2. Create and activate a virtual environment:
   `python -m venv venv`
   `venv\Scripts\Activate.ps1`
3. Install packages:
   `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set MySQL details. If you want SQLite for a quick local test, set `DB_ENGINE=sqlite` or remove the MySQL setting.
5. Apply migrations and create an admin login for the custom CMS:
   `python manage.py migrate`
   `python manage.py createsuperuser`
6. Create starter records:
   `python manage.py seed_demo`
7. Run:
   `python manage.py runserver`
8. Website: `http://127.0.0.1:8000/`
   Custom CMS: `http://127.0.0.1:8000/cms/login/`

## CMS use
- Login with the superuser/staff credentials created in step 5.
- Open **Website Identity & Hero** to edit homepage section text and stats.
- Open **Fleet & Pricing** to add a vehicle. Upload its photo, fill the carousel specifications, tick `Showcase enabled`, and save.
- Open **All Website Sections** to add optional image/text sections and control their order/visibility.
- Open **Testimonials** to manage reviews.

## Notes
- This is a local-development ready project. Configure production `DEBUG=False`, a strong `SECRET_KEY`, allowed hosts, HTTPS, static/media storage and production database before deployment.
- Booking form currently records booking requests in the database; live GPS tracking, payment gateway, SMS/email dispatch and real driver allocation require external services and are not represented as live integrations in this build.


## Latest visual/functionality update (4 Nov 2026)
- Added a dedicated Figma-inspired booking confirmation popup after a successful `/book/` response, including booking reference and Done/Escape/backdrop dismissal.
- Replaced the safety feature text glyphs with consistent inline SVG icon treatments matching the supplied reference.
- Fleet showcase uses the CMS-managed Vehicle image field; add a real vehicle photo for each fleet record in CMS → Fleet & Pricing. The screenshots supplied for this revision are UI references, not standalone vehicle photographs, so no screenshot has been cropped and misrepresented as a car photo.
- Fleet tabs, previous/next arrows and dots are wired to the same active slide state in `static/js/site.js`; vehicle name, description, specs and image are rendered from the selected CMS Vehicle record.


Latest update: saved booking requests now include a WhatsApp click-to-chat action. Configure `WHATSAPP_OWNER_NUMBER` in `backend/.env` (country code + digits). No new database migration is required.
