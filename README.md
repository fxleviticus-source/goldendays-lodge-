# Golden Days Lodges: website (Nova Web Studio demo)

15-page static site (HTML, CSS, vanilla JS). No frameworks, no server needed.

## Pages
Home (with welcome animation) · Lodges hub · 5 lodge pages (Woodlands Main, Buluwe, Makeni, Livingstone, Senanga) · Rooms · Dining · Events · Car Hire · Corporate Stays · Gallery · About · Contact

## Run locally
    cd golden-days
    python3 -m http.server 8000     # open http://localhost:8000

## Edit content
All text, rates, phones, addresses and photos live in **config/site.json**. After editing, regenerate the pages:

    python3 build.py

(Layout/templates are in `build.py`, styling in `css/style.css`, behaviour in `js/main.js`.)

## Deploy
Upload the whole folder to any static host (GitHub Pages, Netlify, cPanel). Then replace `YOUR-DOMAIN` in config/site.json, run `python3 build.py`, and the sitemap/robots files update.

## Where the details came from
Addresses, phone numbers, room types, rates, email and Facebook come from the lodge's current website (goldendayslodge.com). Instagram handle: @golden_days_lodge.

## Needs confirming with the lodge
1. Rates (shown as listed on their current site; marked "confirm when you enquire").
2. Whether each branch phone number is also a WhatsApp number (the enquiry buttons use them). Senanga has no listed number, so its enquiries go to the main line.
3. Which facilities (restaurant, conferencing) each branch actually has; text is currently group-level.
4. **Car Hire page**: wording is generic; confirm the lodge offers vehicles/transfers, or remove the page.
5. Founding story, owners and milestones (About page placeholder).
6. Opening hours, exact map pins, official Instagram/Makeni pages.
7. Real logo files (vector) and real photos.

## Temporary content
- All photos are free-licence Unsplash stock (hotlinked), labelled as stock in the footer and gallery with credits. They are NOT the lodges. Replace via the `images` block in config (or download to `assets/img/`).
- `YOUR-DOMAIN` placeholder in sitemap.xml / robots.txt / JSON-LD.

## Notes
- Enquiry form builds a WhatsApp message (lodge, dates, guests). It is an enquiry, not live availability or a booking.
- Contact form opens the visitor's email app (no backend). Plug in Formspree/Web3Forms later if wanted.
- Welcome animation plays once per session, can be skipped, and is disabled for reduced-motion users.
- Tested at 320, 390, 768 and 1440px: no horizontal overflow, no console errors, one H1 per page. Photos, Google Maps, fonts, Facebook and Instagram could not be loaded in the build sandbox, so check these live.

## Standout features
- Home "Where are you headed?" branch finder (Lusaka / Livingstone / Senanga) with one-tap call buttons.
- Rooms page: tick up to 3 rooms from any lodge to compare side by side (data from config/site.json).
- Mobile bottom bar on every page: Enquire, Call (this lodge, or main line) and WhatsApp.
- Corporate & Group Stays page (wording is generic; confirm the lodge wants it).
