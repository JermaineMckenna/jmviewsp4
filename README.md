# JMViews — Digital Services Studio

JMViews is a one-person digital services studio that brings together **web design & development**, **photography + aerial cinematography**, **video editing/motion**, and **branding** in one place.

The site is designed for clients who want a clean and modern way to **submit a project enquiry**, **track progress**, **download delivered files**, and **pay securely** (deposit + final balance) via Stripe. It also acts as a professional presence for the JMViews brand, showcasing services and providing clear ways to get in touch.

**Live site:**  https://jmviews-p4-1b43f32fc4e1.herokuapp.com/
**Repository:** https://github.com/JermaineMckenna/jmviewsp4

---

## Table of Contents

- [User Experience](#user-experience)
  - [Project Goals](#project-goals)
  - [Target Audience](#target-audience)
  - [User Stories](#user-stories)
- [Design](#design)
  - [Colour Scheme & Typography](#colour-scheme--typography)
  - [Wireframes](#wireframes)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Future Features](#future-features)
- [Database & Data Model](#database--data-model)
- [E-commerce / Payments (Stripe)](#e-commerce--payments-stripe)
- [Testing](#testing)
  - [Manual Testing](#manual-testing)
  - [Validator Testing](#validator-testing)
  - [Known Bugs](#known-bugs)
- [Deployment](#deployment)
  - [Heroku](#heroku)
  - [Local Development](#local-development)
- [Technologies Used](#technologies-used)
- [Credits](#credits)

---

## User Experience

### Project Goals
- Provide a clean public-facing studio site (Home, Services, Portfolio, About, Contact).
- Allow clients to create an account and submit a **new enquiry**.
- Allow clients to view **orders**, read updates, download files, and make **secure payments**.
- Provide a simple admin workflow for managing services, orders, and deliverables.

### Target Audience
- Individuals and small businesses who need:
  - A modern website
  - Photography and drone visuals
  - Short-form video edits
  - Branding/logo assets

### User Stories

**First-time visitor**
- As a visitor, I can view services so I understand what JMViews offers.
- As a visitor, I can navigate easily across pages on desktop and mobile.
- As a visitor, I can contact JMViews directly via email or socials.

**Client**
- As a client, I can register/login to submit an enquiry.
- As a client, I can view my order details and project brief.
- As a client, I can pay a deposit / final balance securely.
- As a client, I can download delivered files once uploaded.

**Admin/Staff**
- As staff, I can manage services displayed on the website.
- As staff, I can view all client orders and update them.
- As staff, I can upload deliverables/files to an order.

---

## Design

### Colour Scheme & Typography
- Dark, modern UI inspired by “studio” style dashboards.
- Accent colour used for calls-to-action and emphasis.
- Clean system font stack for performance and consistency.

### Wireframes
Wireframes are stored in: `documentation/wireframes/`

- Home (Desktop)  
  ![Home Wireframe](documentation/wireframes/<wireframe-file>.jpeg)

- Services (Desktop)  
  ![Services Wireframe](documentation/wireframes/<wireframe-file>.jpeg)

- Orders (Desktop)  
  ![Orders Wireframe](documentation/wireframes/<wireframe-file>.jpeg)

---

## Features

### Existing Features

#### Navigation Bar
- Responsive nav with links to Home, Services, Portfolio, About and Contact.
- Login/Register shown for logged-out users.
- Orders/Logout shown for logged-in users.

![Navbar](documentation/screenshots/navbar.jpeg)

---

#### Home Page
- Studio introduction with CTA buttons.
- Clear paths to Services, Portfolio, and Contact.

![Home](documentation/screenshots/homepage.jpeg)
![home](documentation/screenshots/homepage2.jpeg)
---

#### Services Page
- Four core service cards with “from” pricing.
- Enquiry CTA routes users into the order/enquiry flow.

![Services](documentation/screenshots/<services-desktop>.jpeg)

---

#### Contact Page
- Direct email CTA (mailto link).
- Social links for studio platforms.

![Contact](documentation/screenshots/contact.jpeg)
![contact](documentation/screenshots/contactsocials.jpeg)

---

#### Account Registration & Login
- Users can create accounts and log in to access orders and payments.

![Register](documentation/screenshots/register.jpeg)  
![Login](documentation/screenshots/login.jpeg)

---

#### Orders (Client Dashboard)
- Clients can view a list of their orders.
- Each order includes status, service, and key project details.

![Orders List](documentation/screenshots/orderspage.jpeg)

---

#### Order Detail (Brief, Files, Payments)
- Project brief displayed clearly.
- File downloads appear when deliverables are uploaded.
- Stripe payments supported for deposit and final balance.

![Order Detail](documentation/screenshots/orderspage2.jpeg)
![order detail](documentation/screenshots/stripes.jpeg)

---

#### Admin / Staff Workflow
- Services can be managed via Django admin.
- Orders and deliverables can be managed by staff users.

![Admin](documentation/screenshots/servicesadmin.jpeg)

---

### Future Features
- Portfolio uploads in admin (projects gallery).
- Email notifications when:
  - Deposit/final paid
  - New deliverable uploaded
- More detailed order timeline/status updates.
- Optional messaging thread per order.

![portfolio](documentation/screenshots/portfolio.jpeg)

---

## Database & Data Model

The project uses a relational database via Django ORM.

Typical models include:
- **Service** (name, description, from_price)
- **Order** (service, title, brief, status, budget, timestamps, payment state)
- **Deliverable** (order, file upload, note, timestamp)
- Django **User** model for authentication

![order](documentation/screenshots/ordersadmin.jpeg)
![order](documentation/screenshots/detailorder.jpeg)

---

## E-commerce / Payments (Stripe)

Stripe is used for secure payments:
- Deposit payment (when enabled on an order)
- Final payment (when set by staff)

Payment status is displayed clearly inside the order detail page.

---

## Testing

### Manual Testing
Manual testing evidence is in: `documentation/testing/`

- Navigation links tested on desktop + mobile
- Account creation and login tested
- New enquiry form tested (validation + submission)
- Order detail display tested
- Stripe deposit payment tested in Stripe test mode
- Deliverable upload tested (staff) and download tested (client)

| Feature | Test Action | Expected Result | Result |
|--------|-------------|----------------|--------|
| Register | Create account | Account created and logged in | Pass |
| Login | Login with valid credentials | User redirected to orders | Pass |
| New enquiry | Submit form | Order created | Pass |
| Pay deposit | Click pay deposit | Stripe checkout loads | Pass |
| Download files | Click download | File opens/downloads | Pass |

![testing]()

---

### Validator Testing
- **HTML:** W3C validator (no major errors)
- **CSS:** Jigsaw validator (no major errors)
- **Python:** PEP8 / linter checks (where applicable)

*(Add your final results once you run them.)*

---

### Known Bugs
- Minor layout edge cases on very small mobile widths may require additional tuning.
- If any features are unfinished, list them here clearly and explain the impact.

---

## Deployment

### Heroku

**Steps used to deploy:**
1. Create a Heroku app
2. Set config vars in Heroku:
   - `SECRET_KEY`
   - `DEBUG` (False)
   - `ALLOWED_HOSTS`
   - `DATABASE_URL` (Postgres add-on)
   - `STRIPE_SECRET_KEY`
   - `STRIPE_PUBLISHABLE_KEY`
   - `STRIPE_WEBHOOK_SECRET` (if used)
   - `SITE_URL`
3. Add `requirements.txt`
4. Add a `Procfile`:
   - `web: gunicorn config.wsgi`
5. Run migrations:
   - `heroku run python manage.py migrate -a <app-name>`
6. Create a superuser:
   - `heroku run python manage.py createsuperuser -a <app-name>`
7. Collect static (if needed):
   - `heroku run python manage.py collectstatic --noinput -a <app-name>`

Live site: <YOUR HEROKU URL HERE>

---

### Local Development

1. Clone the repo:
   ```bash
   git clone https://github.com/JermaineMckenna/jmviewsp4.git