# Phase 5: Frontend UI & Templates - Plan

## Goal
Build a premium, cyber-themed frontend interface using Vanilla HTML, Tailwind CSS, and Jinja2 templates.

## Proposed Changes

### Backend Routing
#### [MODIFY] app/main.py
- Add GET endpoints for `/login`, `/register`, and `/dashboard` that return Jinja2 `TemplateResponse`.

### HTML Templates
#### [MODIFY] templates/base.html
- Embed Tailwind CDN and Google Fonts.
- Build a responsive navigation bar.

#### [NEW] templates/index.html
- Hero section for the landing page.

#### [NEW] templates/login.html & templates/register.html
- Auth forms with Vanilla JS interceptors to call `/auth/token` and `/auth/register`.
- Token storage logic (`localStorage.setItem('token', data.access_token)`).

#### [NEW] templates/dashboard.html
- The main email analysis form.
- Vanilla JS to parse the input, send to `POST /analysis`, and render the dynamic Score Card.

## Verification Plan
- Start the server.
- Open `http://localhost:8000` in a browser.
- Visually inspect the aesthetic quality (WOW factor).
- Perform a manual end-to-end test: Register -> Login -> Analyze a phishing email.
