#!/usr/bin/env python3
"""Test two specific suspicious messages through PhishGuard."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analysis.heuristics import EmailAnalyzer

analyzer = EmailAnalyzer()

tests = [
    {
        "id": "MSG-01",
        "name": "Investment scam (USDT passive income)",
        "sender": "Crypto Wealth <info@crypto-wealth.xyz>",
        "subject": "Earn passive income with USDT - 28% daily returns!",
        "body": """Just one phone needed

Only 13 USDT required to earn passively

👥 Invite friends and get up to 15% commission

📈 Daily returns as high as 28% — break even in 3 days!

🔥 Join now and start earning today!

👉 https://www.866698.com/#/register?invite_code=001122""",
        "urls": ["https://www.866698.com/#/register?invite_code=001122"],
    },
    {
        "id": "MSG-02",
        "name": "Ponzi scheme (Celsius Bank AG)",
        "sender": "Celsius Bank <admin@celsius-bank-ag.top>",
        "subject": "Daily returns 28%, start with just 12 USDT!",
        "body": """🔥 Daily returns 28%, start with just 12 USDT!
📱 Mobile operation, invite friends to earn 15% commission
⚡ Celsius Bank AG quant system runs automatically
👉 Join now: https://www.63169.com/#/register?invite_code=556688""",
        "urls": ["https://www.63169.com/#/register?invite_code=556688"],
    },
]

print("=" * 80)
print("  PHISHGUARD — Manual Message Test")
print("=" * 80)
print()

for t in tests:
    print(f"[{t['id']}] {t['name']}")
    print(f"  Sender:  {t['sender']}")
    print(f"  Subject: {t['subject']}")
    print(f"  URLs:    {t['urls']}")
    print()

    result = analyzer.analyze(
        sender=t["sender"],
        subject=t["subject"],
        text_content=t["body"],
        urls=t["urls"],
    )

    score = result["numeric_score"]
    level = result["score_level"]
    just = result["justification"]

    if score >= 70:
        verdict = "🔴 HIGH RISK — PHISHING"
    elif score >= 30:
        verdict = "🟡 MEDIUM RISK — SUSPICIOUS"
    else:
        verdict = "🟢 LOW RISK — LIKELY SAFE"

    print(f"  Score: {score}/100 ({level})")
    print(f"  Verdict: {verdict}")
    print(f"  Justification:")
    for reason in just.split(" | "):
        print(f"    • {reason.strip()}")
    print()
    print("-" * 80)
    print()

print("=" * 80)
