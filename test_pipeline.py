#!/usr/bin/env python3
"""
Test the full pipeline: raw .eml -> parser -> analyzer
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis.parser import parse_email
from analysis.heuristics import EmailAnalyzer

analyzer = EmailAnalyzer()

# Test raw .eml format emails
raw_emails = []

# ── Phishing raw email ──
raw_emails.append({
    "id": "RAW-01",
    "category": "phishing",
    "name": "Raw .eml PayPal phishing",
    "raw": """From: "PayPal" <security@paypa1.com>
To: victim@example.com
Subject: URGENT: Account Suspension Notice
Date: Mon, 10 Jun 2026 08:00:00 +0000
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"

Dear Customer,

Your PayPal account has been suspended due to suspicious activity.

Verify immediately: http://paypa1.com/verify

Failure to act will result in permanent closure.

PayPal Security
""",
})

# ── Legitimate raw email ──
raw_emails.append({
    "id": "RAW-02",
    "category": "legitimate",
    "name": "Raw .eml GitHub notification",
    "raw": """From: GitHub <noreply@github.com>
To: hatim@example.com
Subject: [GitHub] Dependency alert for your repository
Date: Mon, 10 Jun 2026 10:30:00 +0000
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"

Hi @hsami7,

We found a security vulnerability in one of your dependencies.

Repository: hsami7/my-project
Package: lodash
Severity: High

View details: https://github.com/hsami7/my-project/security/dependabot

Thanks,
GitHub
""",
})

# ── HTML email ──
raw_emails.append({
    "id": "RAW-03",
    "category": "phishing",
    "name": "Raw .eml HTML phishing",
    "raw": """From: "Apple ID" <appleid@apple-verify.xyz>
To: user@example.com
Subject: Your Apple ID has been locked
Date: Mon, 10 Jun 2026 12:00:00 +0000
MIME-Version: 1.0
Content-Type: text/html; charset="utf-8"

<html>
<body>
<p>Dear Customer,</p>
<p>Your Apple ID has been locked due to multiple failed sign-in attempts.</p>
<p><a href="http://apple-verify.xyz/unlock">Click here to unlock your account</a></p>
<p>This is urgent. Immediate action required.</p>
<p>Apple Support</p>
</body>
</html>
""",
})

# ── Multipart email ──
raw_emails.append({
    "id": "RAW-04",
    "category": "legitimate",
    "name": "Raw .eml multipart legitimate",
    "raw": """From: Prof. Ahmed Benbrahim <ahmed.benbrahim@uemf.ac.ma>
To: students@uemf.ac.ma
Subject: CS401 - Lecture notes for week 12
Date: Mon, 10 Jun 2026 14:00:00 +0000
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="boundary123"

--boundary123
Content-Type: text/plain; charset="utf-8"

Dear Students,

Please find attached the lecture notes for week 12 on Network Security.

The midterm exam will cover chapters 1-6. Study guide is available on Moodle:
https://moodle.uemf.ac.ma/course/view.php?id=42

Best regards,
Prof. Benbrahim

--boundary123
Content-Type: text/html; charset="utf-8"

<html><body>
<p>Dear Students,</p>
<p>Please find attached the lecture notes for week 12 on Network Security.</p>
<p>The midterm exam will cover chapters 1-6. Study guide is available on Moodle:
<a href="https://moodle.uemf.ac.ma/course/view.php?id=42">https://moodle.uemf.ac.ma/course/view.php?id=42</a></p>
<p>Best regards,<br>Prof. Benbrahim</p>
</body></html>
--boundary123--
""",
})

# ── Malformed email (missing headers) ──
raw_emails.append({
    "id": "RAW-05",
    "category": "phishing",
    "name": "Malformed email with minimal headers",
    "raw": """From: admin@secure-bank.top
Subject: Account verification needed

Dear User,

Your bank account needs verification. Please click:
http://secure-bank.top/verify

This is urgent.
""",
})

print("=" * 80)
print("  FULL PIPELINE TEST: Raw .eml -> Parser -> Analyzer")
print("=" * 80)
print()

for email in raw_emails:
    print(f"  [{email['id']}] {email['name']}")
    print(f"  Expected: {email['category'].upper()}")
    
    try:
        parsed = parse_email(email["raw"])
        sender = parsed["headers"].get("From", "")
        subject = parsed["headers"].get("Subject", "")
        body = parsed["body_text"]
        urls = parsed["urls"]
        
        print(f"  Parsed sender:  {sender}")
        print(f"  Parsed subject: {subject}")
        print(f"  Parsed URLs:    {urls}")
        print(f"  Body length:    {len(body)} chars")
        
        result = analyzer.analyze(sender=sender, subject=subject, text_content=body, urls=urls)
        
        score = result["numeric_score"]
        level = result["score_level"]
        
        if email["category"] == "phishing":
            correct = score >= 50
        elif email["category"] == "legitimate":
            correct = score < 50
        else:
            correct = True
        
        status = "✅ PASS" if correct else "❌ FAIL"
        print(f"  {status} | Score: {score} ({level})")
        print(f"  Reason: {result['justification'][:150]}")
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
    
    print()

print("=" * 80)
