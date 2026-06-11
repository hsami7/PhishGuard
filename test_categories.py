#!/usr/bin/env python3
"""Quick test for the new 3-way category + explanation output."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analysis.heuristics import EmailAnalyzer

analyzer = EmailAnalyzer()

tests = [
    ("Phishing", "PayPal Security <security@paypa1-security.xyz>",
     "URGENT: Your account has been suspended",
     "Dear Customer, verify your password immediately at http://paypa1-security.xyz/verify",
     ["http://paypa1-security.xyz/verify"]),

    ("Legitimate", "GitHub <noreply@github.com>",
     "[GitHub] A new personal access token was added",
     "Hi @user, a new token was added. Review at https://github.com/settings/security",
     ["https://github.com/settings/security"]),

    ("Spam/Junk", "Crypto Wealth <info@crypto-wealth.xyz>",
     "Earn passive income with USDT - 28% daily returns!",
     "📱 Just one phone needed 💰 Only 13 USDT required 👥 Invite friends get up to 15% commission 📈 Daily returns as high as 28% 🔥 Join now! 👉 https://www.866698.com/#/register?invite_code=001122",
     ["https://www.866698.com/#/register?invite_code=001122"]),

    ("Spam/Junk", "Celsius Bank <admin@celsius-bank-ag.top>",
     "Daily returns 28%, start with just 12 USDT!",
     "🔥 Daily returns 28%, start with just 12 USDT! 📱 Mobile operation, invite friends to earn 15% commission ⚡ Celsius Bank AG quant system runs automatically 👉 Join now: https://www.63169.com/#/register?invite_code=556688",
     ["https://www.63169.com/#/register?invite_code=556688"]),
]

print("=" * 80)
print("  PHISHGUARD — 3-Way Category + Explanation Test")
print("=" * 80)

for expected, sender, subject, body, urls in tests:
    result = analyzer.analyze(sender=sender, subject=subject, text_content=body, urls=urls)

    cat = result["category"]
    score = result["numeric_score"]
    level = result["score_level"]

    # Category match check
    cat_ok = (
        (expected == "Phishing" and cat == "phishing") or
        (expected == "Legitimate" and cat == "legitimate") or
        (expected == "Spam/Junk" and cat == "spam_junk")
    )

    status = "✅" if cat_ok else "❌"
    print(f"\n{status} Expected: {expected} | Got: {cat} ({score}/100, {level})")
    print(f"   Sender: {sender}")
    print(f"   Subject: {subject}")
    print(f"\n   📋 EXPLANATION:")
    for line in result["explanation_text"].split("\n"):
        print(f"      {line}")
    print(f"\n   📊 Structured breakdown:")
    for key, vals in result["explanation"].items():
        if vals:
            print(f"      [{key}] {vals}")
    print("-" * 80)
