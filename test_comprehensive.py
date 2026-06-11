#!/usr/bin/env python3
"""
PhishGuard Comprehensive Test Suite
Tests the EmailAnalyzer heuristic + ML engine with diverse email samples.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analysis.heuristics import EmailAnalyzer

analyzer = EmailAnalyzer()

# ──────────────────────────────────────────────────────────────────────
# TEST CASES
# Each: (label, sender, subject, body, urls, expected_category)
# expected_category: "phishing", "legitimate", "junk"
# ──────────────────────────────────────────────────────────────────────

tests = []

# ══════════════════════════════════════════════════════════════════════
# 1. PHISHING E-mails (should score HIGH)
# ══════════════════════════════════════════════════════════════════════

tests.append({
    "id": "PHISH-01",
    "category": "phishing",
    "name": "Classic PayPal credential harvest",
    "sender": "PayPal Security <security@paypa1-security.xyz>",
    "subject": "URGENT: Your account has been suspended",
    "body": """Dear Customer,

We have detected unusual activity on your PayPal account. Your account has been temporarily suspended.

Please verify your identity immediately by clicking the link below:
http://paypa1-security.xyz/verify/login

Failure to verify within 24 hours will result in permanent account closure.

Thank you,
PayPal Security Team""",
    "urls": ["http://paypa1-security.xyz/verify/login"],
})

tests.append({
    "id": "PHISH-02",
    "category": "phishing",
    "name": "Bank spoof with IP URL",
    "sender": "Bank of America <alerts@192.168.1.100>",
    "subject": "Action Required: Verify your bank account",
    "body": """Dear User,

Your Bank of America account requires immediate verification.

Click here to verify: http://192.168.1.100/login.php

This is urgent. Your account will be closed if you do not act now.

Bank of America Security""",
    "urls": ["http://192.168.1.100/login.php"],
})

tests.append({
    "id": "PHISH-03",
    "category": "phishing",
    "name": "Microsoft 365 password reset scam",
    "sender": "Microsoft 365 <noreply@micros0ft-login.top>",
    "subject": "Your password expires today - immediate action required",
    "body": """Dear User,

Your Microsoft 365 password is expiring. To avoid service interruption, please reset your password immediately.

Reset here: http://micros0ft-login.top/password-reset

If you do not reset your password, your account will be suspended.

Microsoft IT Support""",
    "urls": ["http://micros0ft-login.top/password-reset"],
})

tests.append({
    "id": "PHISH-04",
    "category": "phishing",
    "name": "Netflix payment failure",
    "sender": "Netflix <billing@netflix-billing.club>",
    "subject": "Payment Failed - Update your payment method",
    "body": """Dear Customer,

We were unable to process your recent payment. Please update your payment information to avoid service interruption.

Update payment: http://netflix-billing.club/payment/update

Your account will be suspended if you do not update within 48 hours.

Netflix Billing""",
    "urls": ["http://netflix-billing.club/payment/update"],
})

tests.append({
    "id": "PHISH-05",
    "category": "phishing",
    "name": "Display name spoof with @ trick",
    "sender": "Apple Support <support@apple.com@evil-domain.ru>",
    "subject": "Your Apple ID has been locked",
    "body": """Dear Customer,

Your Apple ID has been locked due to suspicious activity.

Verify your account: http://evil-domain.ru/apple/verify

Please act immediately to restore access.

Apple Support Team""",
    "urls": ["http://evil-domain.ru/apple/verify"],
})

tests.append({
    "id": "PHISH-06",
    "category": "phishing",
    "name": "Amazon order confirmation scam",
    "sender": "Amazon <orders@amaz0n-orders.xyz>",
    "subject": "Your Amazon order #402-9981732-110 has been confirmed",
    "body": """Dear Customer,

Thank you for your recent order. Your order total is $849.99.

If you did not place this order, please verify your account immediately:
http://amaz0n-orders.xyz/account/verify

Urgent: Failure to verify will result in charges to your card.

Amazon Orders""",
    "urls": ["http://amaz0n-orders.xyz/account/verify"],
})

tests.append({
    "id": "PHISH-07",
    "category": "phishing",
    "name": "Google Docs phishing",
    "sender": "Google Docs <docs@g0ogle-docs.tk>",
    "subject": "A document has been shared with you - Action Required",
    "body": """Dear User,

Someone has shared an important document with you. Click below to view:
http://g0ogle-docs.tk/shared/document

Please verify your Google account to access the document.

Google Docs Team""",
    "urls": ["http://g0ogle-docs.tk/shared/document"],
})

tests.append({
    "id": "PHISH-08",
    "category": "phishing",
    "name": "Chase bank wire transfer alert",
    "sender": "Chase Bank <alerts@chase-secure.top>",
    "subject": "URGENT: Unauthorized wire transfer detected",
    "body": """Dear Customer,

An unauthorized wire transfer of $5,000 has been initiated from your account.

To cancel this transfer, verify your identity immediately:
http://chase-secure.top/verify/wire

This is urgent. Act now to prevent loss.

Chase Fraud Department""",
    "urls": ["http://chase-secure.top/verify/wire"],
})

tests.append({
    "id": "PHISH-09",
    "category": "phishing",
    "name": "Multiple suspicious URLs",
    "sender": "Security Team <admin@secure-portal.xyz>",
    "subject": "Account verification required - immediate action",
    "body": """Dear User,

Your account needs verification. Please use the links below:

Login: http://secure-portal.xyz/login
Verify: http://secure-portal.xyz/verify
Reset: http://secure-portal.xyz/reset
Confirm: http://secure-portal.xyz/confirm

All links must be completed within 24 hours.

Security Team""",
    "urls": [
        "http://secure-portal.xyz/login",
        "http://secure-portal.xyz/verify",
        "http://secure-portal.xyz/reset",
        "http://secure-portal.xyz/confirm",
        "http://secure-portal.xyz/final",
    ],
})

tests.append({
    "id": "PHISH-10",
    "category": "phishing",
    "name": "Typosquatted domain (gooogle)",
    "sender": "Google Security <security@gooogle.com>",
    "subject": "Suspicious sign-in prevented",
    "body": """Dear Customer,

We prevented a suspicious sign-in to your Google account from a new device.

If this was not you, please secure your account:
http://gooogle.com/security/check

Google Security Team""",
    "urls": ["http://gooogle.com/security/check"],
})

# ══════════════════════════════════════════════════════════════════════
# 2. LEGITIMATE E-mails (should score LOW)
# ══════════════════════════════════════════════════════════════════════

tests.append({
    "id": "LEGIT-01",
    "category": "legitimate",
    "name": "Real GitHub notification",
    "sender": "GitHub <noreply@github.com>",
    "subject": "[GitHub] A new personal access token was added to your account",
    "body": """Hey @user,

A new personal access token (Classic) was added to your account.

If you did not create this token, please review your account security:
https://github.com/settings/security

You can revoke this token at:
https://github.com/settings/tokens

Thanks,
The GitHub Team""",
    "urls": [
        "https://github.com/settings/security",
        "https://github.com/settings/tokens",
    ],
})

tests.append({
    "id": "LEGIT-02",
    "category": "legitimate",
    "name": "Real Amazon order confirmation",
    "sender": "Amazon <shipment-tracking@amazon.com>",
    "subject": "Your Amazon.com order has shipped (#123-4567890-1234567)",
    "body": """Hello Hatim,

Your package is on its way! Track your delivery:
https://www.amazon.com/gp/your-account/order-details

Order #123-4567890-1234567
Estimated delivery: Thursday, June 12

Thanks for shopping with us.
Amazon.com""",
    "urls": [
        "https://www.amazon.com/gp/your-account/order-details",
    ],
})

tests.append({
    "id": "LEGIT-03",
    "category": "legitimate",
    "name": "Real Google security alert",
    "sender": "Google <no-reply@accounts.google.com>",
    "subject": "Security alert - New sign-in from Linux",
    "body": """Hi Hatim,

We noticed a new sign-in to your Google Account on a Linux device. If this was you, you don't need to do anything. If not, we'll help you secure your account.

Check activity: https://myaccount.google.com/device-activity

Google Accounts team""",
    "urls": ["https://myaccount.google.com/device-activity"],
})

tests.append({
    "id": "LEGIT-04",
    "category": "legitimate",
    "name": "University email from professor",
    "sender": "Prof. Ahmed Benbrahim <ahmed.benbrahim@uemf.ac.ma>",
    "subject": "CS401 - Assignment 3 deadline reminder",
    "body": """Dear Students,

This is a reminder that Assignment 3 for CS401 (Network Security) is due next Friday, June 20th at 11:59 PM.

Please submit via the course portal:
https://moodle.uemf.ac.ma/course/view.php?id=42

If you have questions, office hours are Tuesday 2-4 PM.

Best regards,
Prof. Benbrahim""",
    "urls": ["https://moodle.uemf.ac.ma/course/view.php?id=42"],
})

tests.append({
    "id": "LEGIT-05",
    "category": "legitimate",
    "name": "LinkedIn connection request",
    "sender": "LinkedIn <messages-noreply@linkedin.com>",
    "subject": "Sarah Chen wants to connect with you",
    "body": """Hi Hatim,

Sarah Chen would like to connect on LinkedIn.

View invitation: https://www.linkedin.com/mynetwork/invitation-manager/

See Sarah's profile: https://www.linkedin.com/in/sarahchen

LinkedIn Corporation""",
    "urls": [
        "https://www.linkedin.com/mynetwork/invitation-manager/",
        "https://www.linkedin.com/in/sarahchen",
    ],
})

tests.append({
    "id": "LEGIT-06",
    "category": "legitimate",
    "name": "PayPal legitimate transaction",
    "sender": "PayPal <service@paypal.com>",
    "subject": "You sent a payment of $25.00 USD to John Doe",
    "body": """Hello Hatim Sami,

You sent a payment of $25.00 USD to John Doe (john@example.com).

Transaction ID: 8AB12345CD6789012

View transaction details:
https://www.paypal.com/myaccount/transactions/details/8AB12345CD6789012

PayPal""",
    "urls": [
        "https://www.paypal.com/myaccount/transactions/details/8AB12345CD6789012",
    ],
})

tests.append({
    "id": "LEGIT-07",
    "category": "legitimate",
    "name": "Discord verification",
    "sender": "Discord <noreply@discord.com>",
    "subject": "Verify your email address for Discord",
    "body": """Hey!

Please verify your email address to finish setting up your Discord account.

Verify Email: https://discord.com/verify

This link expires in 24 hours.

- Discord""",
    "urls": ["https://discord.com/verify"],
})

tests.append({
    "id": "LEGIT-08",
    "category": "legitimate",
    "name": "Calendar invitation",
    "sender": "Google Calendar <calendar-notification@google.com>",
    "subject": "Invitation: Team standup - Monday 9:00 AM",
    "body": """You have been invited to a meeting.

Event: Team standup
When: Monday, June 16, 2026 at 9:00 AM - 9:30 AM (WEST)
Where: https://meet.google.com/abc-defg-hij

View on Google Calendar: https://calendar.google.com/calendar/event?eid=xyz

Google Calendar""",
    "urls": [
        "https://meet.google.com/abc-defg-hij",
        "https://calendar.google.com/calendar/event?eid=xyz",
    ],
})

# ══════════════════════════════════════════════════════════════════════
# 3. JUNK / SPAM (not phishing but unwanted)
# ══════════════════════════════════════════════════════════════════════

tests.append({
    "id": "JUNK-01",
    "category": "junk",
    "name": "Nigerian prince scam",
    "sender": "Prince Abubakar <prince.abubakar@legitimate-charity.org>",
    "subject": "CONFIDENTIAL BUSINESS PROPOSAL",
    "body": """Dear Friend,

I am Prince Abubakar from Nigeria. I need your help to transfer $15,000,000 USD from my late father's estate.

In return for your assistance, you will receive 30% of the total amount.

Please reply with your bank details and full name to proceed.

God bless you,
Prince Abubakar""",
    "urls": [],
})

tests.append({
    "id": "JUNK-02",
    "category": "junk",
    "name": "Cheap medication spam",
    "sender": "Pharma Deals <deals@best-meds.xyz>",
    "subject": "Buy cheap Viagra and Cialis - 80% OFF!!!",
    "body": """Best prices on medication!

Viagra - $0.99/pill
Cialis - $1.29/pill
Weight loss pills - $0.49/pill

Order now: http://best-meds.xyz/shop

No prescription needed! Worldwide shipping!

Unsubscribe: http://best-meds.xyz/unsubscribe""",
    "urls": ["http://best-meds.xyz/shop", "http://best-meds.xyz/unsubscribe"],
})

tests.append({
    "id": "JUNK-03",
    "category": "junk",
    "name": "Lottery winner spam",
    "sender": "Euro Millions <winner@euromillions-prizes.top>",
    "subject": "CONGRATULATIONS! You have won €2,500,000!!!",
    "body": """Dear Lucky Winner,

Your email address was selected in our random draw. You have won €2,500,000 in the Euro Millions lottery!

To claim your prize, send your full name, address, and phone number to claims@euromillions-prizes.top

Congratulations!
Euro Millions Prize Team""",
    "urls": [],
})

tests.append({
    "id": "JUNK-04",
    "category": "junk",
    "name": "Crypto investment scam",
    "sender": "Crypto Wealth <invest@crypto-wealth.club>",
    "subject": "Make $10,000 per day with Bitcoin - Guaranteed!",
    "body": """Are you tired of working for peanuts?

Our proprietary Bitcoin trading bot guarantees 300% returns in just 7 days!

Join thousands of satisfied investors:
http://crypto-wealth.club/register

Minimum investment: $250
Expected returns: $2,500 in 7 days!

Don't miss out on this limited opportunity!""",
    "urls": ["http://crypto-wealth.club/register"],
})

tests.append({
    "id": "JUNK-05",
    "category": "junk",
    "name": "Work from home spam",
    "sender": "Work From Home Jobs <jobs@remote-income.top>",
    "subject": "Earn $500/day working from home - No experience needed!",
    "body": """Tired of your 9-5 job?

Make $500 per day from the comfort of your home! No experience required.

Sign up now: http://remote-income.top/join

Thousands are already earning. Why not you?

This is not a scam. 100% legitimate opportunity.""",
    "urls": ["http://remote-income.top/join"],
})

# ══════════════════════════════════════════════════════════════════════
# 4. EDGE CASES
# ══════════════════════════════════════════════════════════════════════

tests.append({
    "id": "EDGE-01",
    "category": "legitimate",
    "name": "Empty body, known sender",
    "sender": "GitHub <noreply@github.com>",
    "subject": "Weekly digest",
    "body": "",
    "urls": [],
})

tests.append({
    "id": "EDGE-02",
    "category": "phishing",
    "name": "Phishing with urgency in body only",
    "sender": "Security <security@account-verify.xyz>",
    "subject": "Account notification",
    "body": """Dear Customer,

Your account will be suspended. Immediate action required.

Please verify your password and bank details at:
http://account-verify.xyz/verify

This is urgent. Your account closure is pending.""",
    "urls": ["http://account-verify.xyz/verify"],
})

tests.append({
    "id": "EDGE-03",
    "category": "legitimate",
    "name": "Newsletter with many URLs",
    "sender": "TechCrunch <newsletter@techcrunch.com>",
    "subject": "This Week in Tech: AI Breakthroughs",
    "body": """Here are this week's top stories:

1. OpenAI releases GPT-5: https://techcrunch.com/gpt5
2. Google's new chip: https://techcrunch.com/google-chip
3. Apple Vision Pro 2: https://techcrunch.com/vision-pro
4. Tesla robotaxi: https://techcrunch.com/tesla
5. SpaceX Starship: https://techcrunch.com/spacex
6. Meta's AI glasses: https://techcrunch.com/meta-glasses

Read more at https://techcrunch.com

Unsubscribe: https://techcrunch.com/unsubscribe""",
    "urls": [
        "https://techcrunch.com/gpt5",
        "https://techcrunch.com/google-chip",
        "https://techcrunch.com/vision-pro",
        "https://techcrunch.com/tesla",
        "https://techcrunch.com/spacex",
        "https://techcrunch.com/meta-glasses",
        "https://techcrunch.com",
        "https://techcrunch.com/unsubscribe",
    ],
})

tests.append({
    "id": "EDGE-04",
    "category": "phishing",
    "name": "Subtle phishing - no obvious red flags",
    "sender": "IT Support <it-support@company-it-helpdesk.top>",
    "subject": "Scheduled password rotation notice",
    "body": """Dear Employee,

As part of our quarterly security update, all employees must rotate their passwords by end of week.

Please use the self-service portal to update your credentials:
http://company-it-helpdesk.top/password-portal

If you encounter any issues, please contact the IT helpdesk.

Thank you,
IT Support""",
    "urls": ["http://company-it-helpdesk.top/password-portal"],
})

tests.append({
    "id": "EDGE-05",
    "category": "legitimate",
    "name": "Personal email from friend",
    "sender": "Yassine El Idrissi <yassine.elidrissi@gmail.com>",
    "subject": "Weekend plans?",
    "body": """Hey Hatim!

Are you free this Saturday? A few of us are going to that new café in Gueliz. Let me know if you can make it!

Cheers,
Yassine""",
    "urls": [],
})

tests.append({
    "id": "EDGE-06",
    "category": "phishing",
    "name": "Brand impersonation with display name spoof",
    "sender": "Netflix <no-reply@netfl1x-security.ru>",
    "subject": "We're having trouble with your payment method",
    "body": """Dear Customer,

We encountered an issue processing your recent payment. To avoid service interruption, please update your payment information.

Update now: http://netfl1x-security.ru/payment

Thank you for choosing Netflix.
Netflix Billing""",
    "urls": ["http://netfl1x-security.ru/payment"],
})

# ══════════════════════════════════════════════════════════════════════
# RUN TESTS
# ══════════════════════════════════════════════════════════════════════

print("=" * 80)
print("  PHISHGUARD COMPREHENSIVE TEST REPORT")
print("=" * 80)
print()

results = []

for t in tests:
    result = analyzer.analyze(
        sender=t["sender"],
        subject=t["subject"],
        text_content=t["body"],
        urls=t["urls"],
    )
    
    # Determine if the classification is "correct"
    score = result["numeric_score"]
    level = result["score_level"]
    category = t["category"]
    
    if category == "phishing":
        correct = score >= 50  # Should be Medium/High
    elif category == "legitimate":
        correct = score < 50   # Should be Low/Medium
    else:  # junk
        correct = True  # Junk is acceptable at any score
    
    status = "✅ PASS" if correct else "❌ FAIL"
    
    results.append({
        "id": t["id"],
        "name": t["name"],
        "expected": category,
        "score": score,
        "level": level,
        "justification": result["justification"],
        "correct": correct,
    })
    
    print(f"  {status}  [{t['id']}] {t['name']}")
    print(f"         Expected: {category.upper()} | Score: {score} ({level})")
    print(f"         Reason: {result['justification'][:120]}")
    print()

# ══════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════

print("=" * 80)
print("  SUMMARY")
print("=" * 80)
print()

total = len(results)
passed = sum(1 for r in results if r["correct"])
failed = total - passed

phishing_tests = [r for r in results if r["expected"] == "phishing"]
legit_tests = [r for r in results if r["expected"] == "legitimate"]
junk_tests = [r for r in results if r["expected"] == "junk"]

phish_pass = sum(1 for r in phishing_tests if r["correct"])
legit_pass = sum(1 for r in legit_tests if r["correct"])
junk_pass = sum(1 for r in junk_tests if r["correct"])

print(f"  Total tests:    {total}")
print(f"  Passed:         {passed} ({passed/total*100:.1f}%)")
print(f"  Failed:         {failed} ({failed/total*100:.1f}%)")
print()
print(f"  Phishing:       {phish_pass}/{len(phishing_tests)} correct ({phish_pass/len(phishing_tests)*100:.1f}%)")
print(f"  Legitimate:     {legit_pass}/{len(legit_tests)} correct ({legit_pass/len(legit_tests)*100:.1f}%)")
print(f"  Junk/Spam:      {junk_pass}/{len(junk_tests)} correct ({junk_pass/len(junk_tests)*100:.1f}%)")
print()

if failed > 0:
    print("  FAILED TESTS:")
    for r in results:
        if not r["correct"]:
            print(f"    ❌ [{r['id']}] {r['name']}")
            print(f"       Expected: {r['expected'].upper()} | Got: score={r['score']} ({r['level']})")
            print(f"       Reason: {r['justification'][:150]}")
            print()

# Score distribution
print("  SCORE DISTRIBUTION:")
print(f"    Low (0-29):     {sum(1 for r in results if r['level'] == 'Low')} tests")
print(f"    Medium (30-69): {sum(1 for r in results if r['level'] == 'Medium')} tests")
print(f"    High (70-100):  {sum(1 for r in results if r['level'] == 'High')} tests")
print()

# Average scores by category
avg_phish = sum(r["score"] for r in phishing_tests) / len(phishing_tests)
avg_legit = sum(r["score"] for r in legit_tests) / len(legit_tests)
avg_junk = sum(r["score"] for r in junk_tests) / len(junk_tests)

print("  AVERAGE SCORES BY CATEGORY:")
print(f"    Phishing:       {avg_phish:.1f}")
print(f"    Legitimate:     {avg_legit:.1f}")
print(f"    Junk/Spam:      {avg_junk:.1f}")
print()

print("=" * 80)
