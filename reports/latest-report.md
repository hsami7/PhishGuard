# PhishGuard Email Classification Report
_Generated: 2026-06-11 20:07 UTC_

## Executive Summary

- Total test cases: **4**
- Passed: **3**
- Failed: **1**
- Pass rate: **75.0%**
- Avg response time: **564 ms**

## Test Cases

### 001_basic_phishing_fr
- Expected category: **phishing**
- Actual category: **phishing**
- Expected score: **High**
- Actual: **High (72)**
- Duration: **104 ms**
- Status: **✅ PASS**

#### Analysis Explanation

```
This email shows strong signs of a phishing attempt.
What triggered this classification:
• Urgency tactics: 'urgent' in subject, 'suspend' in body, 'verify' in body
• Content flags: High emoji density: 8 emojis (1.8% of text) — typical of spam/scam
• ML analysis: ML model flagged as phishing (98.4% confidence)
```

### 002_advanced_phishing_brand_impersonation
- Expected category: **phishing**
- Actual category: **phishing**
- Expected score: **High**
- Actual: **High (100)**
- Duration: **2106 ms**
- Status: **✅ PASS**

#### Analysis Explanation

```
This email shows strong signs of a phishing attempt.
What triggered this classification:
• Urgency tactics: 'immediate' in body, 'suspend' in body, 'verify' in subject, 'verify' in body
• URL problems: URL contains raw IP address
• Content flags: Generic greeting (Dear Customer / Dear User)
• ML analysis: ML model flagged as phishing (99.8% confidence)
```

### 003_legitimate_internal
- Expected category: **legitimate**
- Actual category: **spam_junk**
- Expected score: **Low**
- Actual: **Medium (34)**
- Duration: **18 ms**
- Status: **❌ FAIL**

#### Analysis Explanation

```
This email appears to be spam or unsolicited junk.
What triggered this classification:
• Content flags: High emoji density: 12 emojis (2.7% of text) — typical of spam/scam
• ML analysis: ML model flagged as phishing (97.8% confidence)
```

### 004_spam_lottery_promo
- Expected category: **spam_junk**
- Actual category: **spam_junk**
- Expected score: **High**
- Actual: **Medium (69)**
- Duration: **30 ms**
- Status: **✅ PASS**

#### Analysis Explanation

```
This email appears to be spam or unsolicited junk.
What triggered this classification:
• Suspicious sender: Suspicious sender domain TLD (.xyz)
• Urgency tactics: 'action required' in body
• ML analysis: ML model flagged as phishing (99.1% confidence)
```

## Recommendations

- Review category decision thresholds to handle edge cases like weak heuristic + strong ML confidence.

---

_Raw outputs saved under: `/home/ubuntu/MYP/PhishGuard/reports/raw/`_
_End of report_
