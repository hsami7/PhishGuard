# PhishGuard Test Report

**Date:** June 11, 2026  
**Tester:** Ron Agent (Automated Test Suite)  
**System Under Test:** PhishGuard v1.0 — Email Phishing Detection Platform  
**Test Scope:** Heuristic engine + ML classifier + Email parser (terminal-only, no browser)

---

## 1. Executive Summary

PhishGuard was tested with **34 email samples** across 4 categories: phishing (13), legitimate (11), junk/spam (5), and edge cases (5). The system achieved an **overall accuracy of 97.1%** (33/34 tests passed).

| Category | Tests | Passed | Accuracy |
|----------|-------|--------|----------|
| Phishing | 13 | 13 | **100%** |
| Legitimate | 11 | 10 | **90.9%** |
| Junk/Spam | 5 | 5 | **100%** |
| Edge Cases | 5 | 5 | **100%** |
| **TOTAL** | **34** | **33** | **97.1%** |

---

## 2. Architecture Overview

PhishGuard uses a **hybrid detection approach**:

1. **Rule-Based Heuristic Engine** (`analysis/heuristics.py`) — 267 lines
   - Suspicious TLD detection (.xyz, .top, .click, .club, .ru, .cn)
   - Raw IP address detection in sender and URLs
   - Display name spoofing detection (brand impersonation, @-trick)
   - Typosquatting detection (Levenshtein distance ≤ 2 against known brands)
   - Urgency keyword scanning (subject + body, weighted differently)
   - Generic greeting detection ("Dear Customer", "Dear User")
   - Excessive URL counting (>3 URLs)
   - PhishTank database lookup (SQLite)
   - URL unshortening (HTTP HEAD with redirect following)
   - Legitimate brand trust heuristic (sender domain matches all link destinations → score reduction)

2. **ML Classifier** (`analysis/email_classifier.pkl` + `vectorizer.pkl`)
   - Logistic Regression with L1 regularization (Lasso)
   - TF-IDF vectorization (5,000 max features, English stop words)
   - Trained on combined datasets: spam_ham_dataset + Phishing_validation_emails + Phishing_Email.csv
   - Only activates on emails with ≥ 8 words (avoids false positives on short text)
   - Contributes up to 30 points when spam confidence ≥ 70%

3. **Email Parser** (`analysis/parser.py`) — 107 lines
   - Raw .eml parsing with Python `email` module (policy.default)
   - Header extraction (From, To, Subject, Date, Return-Path)
   - Body extraction (text/plain + text/html, multipart support)
   - URL regex harvesting with deduplication
   - Malformed email tolerance (best-effort parsing)

---

## 3. Detailed Test Results

### 3.1 Phishing Detection (13/13 — 100%)

All phishing emails were correctly identified with **average score of 94.5/100**.

| ID | Type | Score | Key Detections |
|----|------|-------|----------------|
| PHISH-01 | PayPal credential harvest | 100 | Display name spoof + .xyz TLD + urgency keywords |
| PHISH-02 | Bank spoof with IP | 100 | Display name spoof + raw IP sender + IP URL |
| PHISH-03 | Microsoft 365 scam | 100 | Display name spoof + .top TLD + urgency |
| PHISH-04 | Netflix payment failure | 79 | .club TLD + suspend keyword + ML classifier |
| PHISH-05 | Display name @-trick | 89 | .ru TLD + urgency keywords |
| PHISH-06 | Amazon order scam | 100 | Display name spoof + .xyz TLD + urgency |
| PHISH-07 | Google Docs phishing | 100 | Display name spoof + action required |
| PHISH-08 | Chase wire transfer | 100 | .top TLD + multiple urgency keywords |
| PHISH-09 | Multiple suspicious URLs | 100 | .xyz TLD + excessive URLs + urgency |
| PHISH-10 | Typosquatting (gooogle) | 100 | Levenshtein distance=1 + display name spoof |
| EDGE-02 | Urgency in body only | 100 | .xyz TLD + multiple urgency keywords |
| EDGE-04 | Subtle phishing | 60 | .top TLD + password keyword + ML classifier |
| EDGE-06 | Brand impersonation | 100 | Display name spoof + .ru TLD + generic greeting |

**Key observation:** The system is extremely aggressive at catching phishing. Even the "subtle" phishing test (EDGE-04) scored 60/100 (Medium risk), which is correct.

### 3.2 Legitimate Email Detection (10/11 — 90.9%)

Legitimate emails scored **average of 10.2/100**.

| ID | Type | Score | Notes |
|----|------|-------|-------|
| LEGIT-01 | GitHub notification | 21 | ML flagged as spam (71.8%) but no heuristic hits → Low |
| LEGIT-02 | Amazon order | 0 | Brand trust heuristic activated (domain matches links) |
| LEGIT-03 | Google security alert | 0 | Clean — no threats detected |
| LEGIT-04 | University email | 0 | ML: 99.9% legitimate confidence |
| LEGIT-05 | LinkedIn connection | 0 | Clean — no threats detected |
| LEGIT-06 | PayPal transaction | 0 | Brand trust heuristic activated |
| **LEGIT-07** | **Discord verification** | **58** | **FALSE POSITIVE** — "verify" keyword triggered |
| LEGIT-08 | Calendar invitation | 0 | Brand trust heuristic activated |
| EDGE-01 | Empty body, known sender | 0 | ML: 100% legitimate |
| EDGE-03 | Newsletter (many URLs) | 33 | Excessive URLs triggered, but not phishing-level |
| EDGE-05 | Personal email | 0 | Clean |

### 3.3 Junk/Spam Detection (5/5 — 100%)

Junk emails scored **average of 55.0/100** (Medium risk).

| ID | Type | Score | Notes |
|----|------|-------|-------|
| JUNK-01 | Nigerian prince | 39 | "bank" keyword + ML classifier |
| JUNK-02 | Cheap medication | 60 | .xyz TLD + ML classifier |
| JUNK-03 | Lottery winner | 58 | .top TLD + ML classifier |
| JUNK-04 | Crypto scam | 59 | .club TLD + ML classifier |
| JUNK-05 | Work from home | 59 | .top TLD + ML classifier |

### 3.4 Full Pipeline Tests (5/5 — 100%)

Raw .eml format emails were parsed and analyzed correctly:
- Plain text phishing ✅
- Plain text legitimate ✅
- HTML phishing ✅
- Multipart (plain + HTML) legitimate ✅
- Malformed/minimal headers phishing ✅

---

## 4. Strengths

### 4.1 Excellent Phishing Detection (100%)
The system catches every phishing email in the test set. The multi-layered approach (heuristics + ML) creates defense in depth — even if one layer misses, another catches it.

### 4.2 Advanced Spoofing Detection
The display name spoofing detection is sophisticated:
- Detects brand names in display names that don't match the sender domain
- Catches the `@` symbol trick in display names
- Uses Levenshtein distance for typosquatting (edit distance 1-2)

### 4.3 Brand Trust Heuristic
The legitimate brand trust system is smart: when sender domain is a known brand (paypal.com, google.com, etc.) AND all URLs link to that same domain, the score is reduced by 40 points. This significantly reduces false positives for real emails from major services.

### 4.4 ML + Heuristic Hybrid
The combination of rule-based heuristics with ML classification provides robustness. The ML model catches patterns that rules miss (like EDGE-04 subtle phishing), while the rules catch structural red flags that ML might overlook.

### 4.5 Robust Email Parser
The parser handles:
- Plain text and HTML emails
- Multipart emails (mixed content types)
- Malformed emails with minimal headers
- Various character encodings
- URL extraction with deduplication

### 4.6 Score Capping and Leveling
Scores are properly capped at 0-100, and the three-tier level system (Low/Medium/High) provides clear risk communication.

---

## 5. Weaknesses

### 5.1 FALSE POSITIVE: "Verify" Keyword Over-Sensitivity
**The only failed test (LEGIT-07):** Discord's legitimate verification email scored 58 (Medium risk) because the word "verify" appears in both the subject and body. The system added +20 for the subject keyword and +10 for the body keyword, plus the ML classifier flagged it at 95.7% spam confidence.

**Impact:** Legitimate verification emails from Discord, and potentially other services, will be flagged as suspicious.

**Root cause:** "verify" is in the urgency_keywords list, but it's also a common word in legitimate security communications.

### 5.2 ML Model False Positives on Security Emails
The ML classifier flagged GitHub's security notification (LEGIT-01) as spam with 71.8% confidence. This didn't cause a failure (score stayed at 21, Low), but it shows the ML model has a bias toward flagging security-related vocabulary as phishing.

### 5.3 Suspicious TLD List is Limited
Only 6 TLDs are flagged: `.xyz`, `.top`, `.click`, `.club`, `.ru`, `.cn`. Many other suspicious TLDs are missing: `.tk`, `.ml`, `.ga`, `.cf`, `.gq`, `.pw`, `.work`, `.date`, `.racing`, `.win`, `.bid`, `.stream`, etc.

### 5.4 No SPF/DKIM/DMARC Analysis
The system doesn't check email authentication headers (SPF, DKIM, DMARC). These are critical signals for detecting spoofed emails. A phishing email that passes SPF/DKIM would be harder to detect.

### 5.5 PhishTank Database Dependency
The PhishTank lookup uses a local SQLite database (`phishguard.db`). If the database is empty or outdated, this entire detection layer is disabled. The test didn't verify if the database actually contains entries.

### 5.6 URL Unshortening is Synchronous and Slow
The `_unshorten_url` method makes HTTP HEAD requests synchronously for each URL. With many URLs, this could slow down analysis significantly. There's also no caching — the same URL would be unshortened repeatedly.

### 5.7 No Attachment Analysis
The system doesn't analyze email attachments (malicious PDFs, executable files, macro-enabled documents). This is a significant gap since many phishing attacks use malicious attachments.

### 5.8 Generic Greeting Detection is Limited
Only two patterns are checked: "dear customer" and "dear user". Other common phishing greetings like "dear valued customer", "dear account holder", "dear member", "attention:", etc. are not detected.

### 5.9 No Language Detection
The system doesn't detect the language of the email. Phishing emails in different languages (Arabic, French, etc.) might not match the English-centric keyword lists.

### 5.10 Score Thresholds May Need Tuning
The current thresholds are: Low (0-29), Medium (30-69), High (70-100). The "verify" false positive scored 58, which is close to the Medium/High boundary. Adjusting thresholds or keyword weights could reduce false positives.

---

## 6. Recommendations for Improvement

### Priority 1 (High Impact)
1. **Refine the "verify" keyword** — Either remove it from urgency_keywords or reduce its weight. Consider context-aware scoring: "verify" in a URL context is more suspicious than in body text.
2. **Expand the suspicious TLD list** — Add `.tk`, `.ml`, `.ga`, `.cf`, `.gq`, `.pw`, `.work`, `.date`, `.racing`, `.win`, `.bid`, `.stream`, `.loan`, `.men`, `.review`.
3. **Add SPF/DKIM/DMARC header analysis** — Parse `Authentication-Results` headers and flag emails that fail authentication checks.

### Priority 2 (Medium Impact)
4. **Implement attachment analysis** — Check file extensions (.exe, .scr, .js, .vbs, .docm, .xlsm), analyze PDFs for JavaScript, and flag suspicious attachments.
5. **Expand generic greeting detection** — Add patterns: "dear valued customer", "dear account holder", "dear member", "attention:", "dear sir/madam".
6. **Add URL reputation scoring** — Beyond PhishTank, check URL age (newly registered domains are more suspicious), domain entropy (random-looking domains), and URL path analysis.
7. **Implement URL unshortening cache** — Cache results to avoid repeated HTTP requests for the same URL.

### Priority 3 (Lower Impact)
8. **Add language detection** — Use `langdetect` or similar to detect email language and apply language-specific keyword lists.
9. **Improve ML model training** — Add more legitimate security emails to the training set to reduce false positives on verification emails.
10. **Add sender reputation tracking** — Track sender history and flag first-time senders as slightly more suspicious.
11. **Implement HTML analysis** — Parse HTML emails for hidden text, suspicious form actions, and pixel tracking.
12. **Add homograph attack detection** — Detect Unicode characters that look like ASCII (e.g., Cyrillic 'а' vs Latin 'a') in sender domains.

---

## 7. Conclusion

PhishGuard is a **well-designed phishing detection system** that demonstrates strong performance across diverse test scenarios. The hybrid heuristic + ML approach is effective, achieving 97.1% accuracy on a comprehensive test set of 34 emails.

The system's **greatest strength** is its multi-layered detection approach — combining structural analysis (TLDs, IPs, spoofing), content analysis (urgency keywords, generic greetings), brand protection (typosquatting, display name spoofing), and machine learning. This defense-in-depth strategy means that even if an attacker evades one layer, others will likely catch the threat.

The **primary weakness** is the over-sensitivity to certain keywords like "verify", which causes false positives on legitimate security communications. This can be addressed through keyword weight tuning and context-aware scoring.

With the recommended improvements — particularly SPF/DKIM analysis, attachment scanning, and expanded TLD coverage — PhishGuard could achieve near-production-grade phishing detection capability.

**Overall Grade: A-** (Excellent foundation, minor tuning needed for production use)
