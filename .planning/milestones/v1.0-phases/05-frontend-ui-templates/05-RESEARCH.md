# Phase 5: Frontend UI & Templates - Research

## Technical Approach

**Core Concept**: 
The frontend will be completely server-rendered initially by FastAPI (Jinja2), but augmented with Vanilla JS for dynamic state (handling JWTs and making asynchronous fetch calls). We will use Tailwind CSS via CDN for rapid, premium styling.

**Aesthetic Guidelines**:
- **Theme**: Cyber-security focus. Dark backgrounds (e.g., `bg-slate-900`) with vibrant neon accents (electric blue `text-cyan-400`, neon green `text-emerald-400` for low risk, deep red `text-rose-500` for high risk).
- **Typography**: Google Fonts 'Inter' or 'Outfit' for a clean, modern, and technical look.
- **Components**: Glassmorphism (translucent backgrounds with `backdrop-blur-md`), soft glows, and rounded corners.
- **Micro-Animations**: Hover states that gently scale up buttons (`hover:scale-105`), smooth transitions (`transition-all duration-300`), and focus rings on inputs to make the app feel alive and responsive.

**Page Structure**:
- `base.html`: Contains the `<head>`, Tailwind CDN, fonts, and a responsive top navigation bar.
- `index.html`: A striking landing page explaining PhishGuard's heuristic power.
- `login.html` & `register.html`: Clean, glassmorphic auth forms. Javascript will catch the submit event, call the REST API, store the resulting `access_token` in `localStorage`, and redirect to `/dashboard`.
- `dashboard.html`: The core tool. A protected view where users paste email details. JS will fetch the `/analysis/` endpoint using the stored token and dynamically render the risk score card.
