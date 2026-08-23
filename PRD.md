# PRD — MedAtlas (ميد أطلس) — Bilingual Medical Devices Atlas

## Original Problem Statement
"صمم لي موقع يقوم بعرض جميع الأجهزة الطبية مع شرح عن كل جهاز وسعره وطبيعة عمله والقطع المكون منها"
(Build a website that displays all medical devices with an explanation of each device, its price, how it works, and its components.)

## User Personas
- Hospital procurement officers comparing devices and budgets
- Biomedical engineers researching device internals
- Arabic- and English-speaking clinicians/visitors browsing equipment

## Architecture
- **Backend**: FastAPI (`/app/backend/server.py`) + MongoDB (motor). Routes under `/api`:
  - `GET /api/meta` — categories, departments (bilingual labels), price bounds, count
  - `GET /api/devices` — filters: `search` (AR+EN regex), `category`, `department`, `min_price`, `max_price`, `sort` (featured/price_asc/price_desc/name)
  - `GET /api/devices/{id}` — full detail (description, principle, components, specs)
  - Startup seed: upserts 13 bilingual device docs (idempotent)
- **Frontend**: React 19 + Tailwind + framer-motion + lenis + react-fast-marquee
  - `context/LanguageContext.jsx` — AR/EN toggle, dir=rtl/ltr on `<html>`, font swap (Alexandria/IBM Plex Sans Arabic ↔ Cabinet Grotesk/IBM Plex Sans), localized price formatting
  - Components: Navbar, Hero (masked line reveal + parallax), Marquee, Catalog (search/filter/sort grid), DeviceCard, Manifesto (dark, numbered chapters, noise texture), TrustSection, Footer, DeviceImage (fallback)
  - Pages: Home, DeviceDetail (`/device/:id`)

## Design System
Swiss high-contrast: bone `#FDFDFD`, ink `#0A0A0A`, electric blue `#0044EE`, signal red `#FF3B30`; 1px flat borders, no shadows/glass; logical properties (ps/pe/start/end) for full RTL support; noise texture on dark sections; spotlight radial on product images.

## Core Requirements (static)
1. Display all medical devices (hospital + clinic mix)
2. Per device: explanation, price, working principle, component parts
3. Bilingual AR/EN with RTL
4. Search + filter by type / price / usage(department)
5. Database-backed catalog

## Implemented (2026-08-21)
- All 5 core requirements: 13 devices seeded (MRI, CT, 4D ultrasound, digital X-ray, ECG, patient monitor, ICU ventilator, AED, infusion pump, anesthesia workstation, surgical robot, hemodialysis, hematology analyzer), each with AR+EN description, working principle, 6 components, 4 specs, price
- Kinetic hero (masked line-by-line reveal), editorial marquee, dark numbered manifesto, parallax hero image, Lenis smooth scroll
- Full filter bar (search w/ debounce, category chips, department select, price slider, sort) against live API
- Device detail pages with specs table
- Verified: API filters (AR search, price+department combos, 404), UI flows (search, card→detail, lang toggle) via curl + screenshots

## Backlog
- P1: Contact/inquiry form per device (Resend email)
- P1: Admin panel to add/edit devices without code
- P2: Device comparison view (side-by-side specs)
- P2: Favorites/shortlist with localStorage
- P2: More devices per category; PDF spec-sheet download

## Test Credentials
No authentication in this app. See /app/memory/test_credentials.md.
