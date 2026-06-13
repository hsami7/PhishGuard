"""Take screenshots of PhishGuard dashboard pages."""
import asyncio
import os
from playwright.async_api import async_playwright

SCREENSHOTS_DIR = "/home/ubuntu/MYP/PhishGuard/reports/screenshots"
BASE_URL = "http://127.0.0.1:8000"

async def take_screenshots():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = await browser.new_context(viewport={'width': 1280, 'height': 900})
        page = await context.new_page()

        # --- 1. Landing Page ---
        print("📸 Landing page...")
        await page.goto(f"{BASE_URL}/")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "01-landing-page.png"))
        print("  ✅ 01-landing-page.png")

        # --- 2. Register Page ---
        print("📸 Register page...")
        await page.goto(f"{BASE_URL}/register")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "02-register-page.png"))
        print("  ✅ 02-register-page.png")

        # --- 3. Login Page ---
        print("📸 Login page...")
        await page.goto(f"{BASE_URL}/login")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "03-login-page.png"))
        print("  ✅ 03-login-page.png")

        # --- 4. Register a test user, then login ---
        print("📝 Registering test user via API...")
        import aiohttp
        async with aiohttp.ClientSession() as session:
            r = await session.post(f"{BASE_URL}/auth/register", json={
                "username": "screenshot_demo",
                "email": "demo@screenshot.com",
                "password": "DemoPass123!"
            })
            if r.status not in (200, 201):
                print(f"  ⚠️ Register failed: {r.status}, trying login anyway")

        print("📸 Dashboard (empty state)...")
        await page.goto(f"{BASE_URL}/login")
        await page.wait_for_load_state("networkidle")
        # Login page has: input#text-0 (first text) and input#password-0 (password)
        # Let me just find by type
        await page.fill('input[type="text"]', 'screenshot_demo')
        await page.fill('input[type="password"]', 'DemoPass123!')
        # Click the login button
        await page.click('button[type="submit"]')
        await page.wait_for_url("**/dashboard", timeout=10000)
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "04-dashboard-empty.png"))
        print("  ✅ 04-dashboard-empty.png")

        # --- 5. Phishing Email Analysis ---
        print("📸 Analysis result (phishing)...")
        await page.fill('#sender', 'The Team at paypal <support@paypall.com>')
        await page.fill('#raw_email', """Subject: Urgent: Account Verification Required

Dear Ron,

We noticed your account on our platform has been inactive for some time and we wanted to ensure everything is in order.

To verify that it's really you, please click the link below within 24 hours:

http://paypall.com/verify-account

If you have any questions, feel free to reply directly to this email.

Best regards,
The Team at paypal""")

        await page.click('#submit-btn')
        await page.wait_for_timeout(3000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "05-analysis-phishing.png"))
        print("  ✅ 05-analysis-phishing.png")

        # --- 6. Scroll to history ---
        print("📸 History table...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "06-history-table.png"))
        print("  ✅ 06-history-table.png")

        # --- 7. Legitimate Email ---
        print("📸 Analysis result (legitimate)...")
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(500)
        await page.click('#clear-btn')
        await page.wait_for_timeout(500)

        await page.fill('#sender', 'GitHub <noreply@github.com>')
        await page.fill('#raw_email', """Subject: [GitHub] Your security alert

Hi there,

We noticed a new sign-in to your GitHub account from a new device.

Device: Chrome on macOS
Location: Rabat, Morocco

If this was you, you can safely ignore this email.
If this wasn't you, please secure your account at:
https://github.com/sessions/security

Thanks,
The GitHub Team""")

        await page.click('#submit-btn')
        await page.wait_for_timeout(3000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "07-analysis-legitimate.png"))
        print("  ✅ 07-analysis-legitimate.png")

        # --- 8. Search/filter ---
        print("📸 Search/filter in history...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        await page.select_option('#history-search-category', 'phishing')
        await page.click('#history-search-btn')
        await page.wait_for_timeout(1500)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "08-history-search.png"))
        print("  ✅ 08-history-search.png")

        await browser.close()
        print(f"\n✅ All 8 screenshots saved to {SCREENSHOTS_DIR}/")

asyncio.run(take_screenshots())
