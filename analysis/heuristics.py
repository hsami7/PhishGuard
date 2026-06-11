import re
import requests
import sqlite3
import email.utils
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class EmailAnalyzer:
    def __init__(self):
        self.suspicious_tlds = ['.xyz', '.top', '.click', '.club', '.ru', '.cn', '.tk', '.ml', '.ga', '.cf', '.gq', '.pw', '.work', '.loan', '.men', '.review', '.stream', '.bid', '.win', '.date', '.racing', '.buzz', '.vip', '.party', '.trade', '.webcam', '.cricket', '.link', '.click', '.download', '.racing', '.science', '.trade']
        self.urgency_keywords = ['urgent', 'immediate', 'password', 'bank', 'suspend', 'action required', 'verify', 'account closure']
        self.scam_keywords = ['passive income', 'daily returns', 'commission', 'invite friends', 'referral', 'guaranteed', 'risk-free', 'no experience', 'work from home', 'earn daily', 'earn passive', 'pyramid', 'ponzi', 'investment opportunity', 'double your money', 'get rich', 'financial freedom', 'limited spots', 'act now', 'join now', 'sign up bonus', 'mining', 'staking', 'apy', 'apy%', 'usdt', 'bitcoin investment', 'crypto investment', 'quant trading', 'trading bot', 'automated trading']
        
        # Load ML model and vectorizer
        self.ml_model = None
        self.ml_vectorizer = None
        self._load_ml_model()
    
    def _load_ml_model(self):
        """Load the trained ML classifier and TF-IDF vectorizer from disk."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "email_classifier.pkl")
        vectorizer_path = os.path.join(current_dir, "vectorizer.pkl")
        
        try:
            with open(model_path, "rb") as f:
                self.ml_model = pickle.load(f)
            with open(vectorizer_path, "rb") as f:
                self.ml_vectorizer = pickle.load(f)
            logger.info("ML email classifier loaded successfully.")
        except FileNotFoundError:
            logger.warning("ML model files not found. ML predictions will be skipped.")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
    
    def _ml_predict(self, text: str) -> dict:
        """Use the ML model to predict if the email text is spam/phishing.
        
        Returns a dict with 'is_spam' (bool), 'confidence' (float 0-1),
        or None if the model is not available.
        """
        if self.ml_model is None or self.ml_vectorizer is None:
            return None
        
        # Skip ML classification on extremely short inputs (less than 8 words)
        # to avoid false positive TF-IDF predictions on single words/phrases.
        clean_text = re.sub(r'<[^>]+>', ' ', text)
        words = [w for w in clean_text.split() if w.strip()]
        if len(words) < 8:
            return {
                "is_spam": False,
                "confidence": 0.0
            }
        
        try:
            text_vec = self.ml_vectorizer.transform([text])
            prediction = self.ml_model.predict(text_vec)[0]
            probabilities = self.ml_model.predict_proba(text_vec)[0]
            spam_confidence = probabilities[1]  # probability of class 1 (spam)
            return {
                "is_spam": bool(prediction == 1),
                "confidence": round(float(spam_confidence), 4)
            }
        except Exception as e:
            logger.error(f"ML prediction failed: {e}")
            return None
    
    def _unshorten_url(self, url: str) -> str:
        try:
            session = requests.Session()
            session.max_redirects = 5
            response = session.head(url, allow_redirects=True, timeout=5)
            return response.url
        except Exception:
            return url

    def _check_phishtank(self, url: str) -> bool:
        try:
            conn = sqlite3.connect("phishguard.db")
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM phishtank_urls WHERE url = ?", (url,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except sqlite3.Error:
            return False

    def _detect_spoofing(self, sender: str) -> tuple[bool, str]:
        display_name, email_addr = email.utils.parseaddr(sender)
        display_name = display_name.lower()
        if not display_name or not email_addr:
            return False, ""
        
        domain = email_addr.split('@')[-1] if '@' in email_addr else ""
        
        # Check if display name has an @ sign (often used to trick users)
        if '@' in display_name:
            return True, "Display name contains '@' symbol to spoof email address"
            
        high_profile_brands = ['paypal', 'apple', 'microsoft', 'google', 'amazon', 'bank of america', 'chase', 'netflix']
        for brand in high_profile_brands:
            if brand in display_name and brand not in domain:
                return True, f"Display name mimics brand '{brand}' but domain does not match"
                
        return False, ""

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
            
        return previous_row[-1]

    def _detect_typosquatting(self, sender: str) -> tuple[bool, str]:
        display_name, email_addr = email.utils.parseaddr(sender)
        if not email_addr or '@' not in email_addr:
            return False, ""
        
        domain_full = email_addr.split('@')[-1].lower()
        domain_parts = domain_full.split('.')
        if len(domain_parts) < 2:
            return False, ""
        
        high_profile_brands = ['paypal', 'apple', 'microsoft', 'google', 'amazon', 'chase', 'netflix']
        for part in domain_parts:
            # Skip common short TLDs/subdomains
            if part in ['com', 'org', 'net', 'edu', 'gov', 'co', 'uk', 'io', 'info', 'biz', 'us', 'www', 'mail', 'email']:
                continue
            for brand in high_profile_brands:
                if part == brand:
                    continue  # Perfect match
                
                dist = self._levenshtein_distance(part, brand)
                if dist in [1, 2]:
                    return True, f"Domain part '{part}' typosquats high-profile brand '{brand}' (edit distance: {dist})"
        return False, ""
    
    def analyze(self, sender: str, subject: str, text_content: str, urls: list[str]):
        score = 0
        # Structured explanation: group triggers by category
        explanation = {
            "spoofing": [],
            "suspicious_sender": [],
            "urgency": [],
            "scam_keywords": [],
            "url_issues": [],
            "content_flags": [],
            "ml_analysis": [],
            "brand_trust": [],
        }

        sender_lower = sender.lower()
        subject_lower = subject.lower()
        body_lower = text_content.lower()

        # ── 1. Spoofing Detection ──
        is_spoofed, spoof_justification = self._detect_spoofing(sender)
        if is_spoofed:
            score += 40
            explanation["spoofing"].append(spoof_justification)

        # ── 2. Typosquatting Detection ──
        is_typosquat, typosquat_justification = self._detect_typosquatting(sender)
        if is_typosquat:
            score += 40
            explanation["spoofing"].append(typosquat_justification)

        # ── 3. Sender TLD & IP Heuristics ──
        for tld in self.suspicious_tlds:
            if sender_lower.endswith(tld) or f"{tld}>" in sender_lower:
                score += 30
                explanation["suspicious_sender"].append(f"Suspicious sender domain TLD ({tld})")
                break

        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        if re.search(ip_pattern, sender):
            score += 30
            explanation["suspicious_sender"].append("Sender contains raw IP address")

        # ── 4. Urgency Keywords ──
        for keyword in self.urgency_keywords:
            if keyword in subject_lower:
                score += 20
                explanation["urgency"].append(f"'{keyword}' in subject")
            if keyword in body_lower:
                score += 10
                explanation["urgency"].append(f"'{keyword}' in body")

        # ── 5. Generic Greeting ──
        if "dear customer" in body_lower or "dear user" in body_lower:
            score += 10
            explanation["content_flags"].append("Generic greeting (Dear Customer / Dear User)")

        # ── 6. Scam / Investment Fraud Keywords ──
        scam_hits = []
        for keyword in self.scam_keywords:
            if keyword in body_lower or keyword in subject_lower:
                scam_hits.append(keyword)
        if scam_hits:
            scam_score = min(len(scam_hits) * 15, 45)
            score += scam_score
            explanation["scam_keywords"].append(
                f"Detected {len(scam_hits)} scam keyword(s): {', '.join(scam_hits[:8])}"
            )

        # ── 7. Emoji Density ──
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002702-\U000027B0"
            "\U00002460-\U000024FF"  # Enclosed Alphanumerics (① ② ③ … ⓪)
            "\U00002500-\U0000257F"  # Box Drawing
            "\U00002580-\U0000259F"  # Block Elements
            "\U00002600-\U000026FF"  # Misc Symbols
            "]+",
            flags=re.UNICODE,
        )

        def _count_emojis(s: str) -> int:
            """Count emoji groups; ignore HTML tags so markup doesn't inflate counts."""
            cleaned = re.sub(r'<[^>]+>', ' ', s)
            return len(emoji_pattern.findall(cleaned))

        full_text = f"{subject} {text_content}"
        emoji_count = _count_emojis(full_text)
        word_count = len([w for w in re.split(r'\s+', full_text.strip()) if w])
        if word_count > 0 and emoji_count >= 5:
            emoji_score = min(int((emoji_count / word_count) * 2000), 20)
            score += emoji_score
            explanation["content_flags"].append(
                f"High emoji density: {emoji_count} emojis across ~{word_count} words — typical of spam/scam"
            )

        # ── 8. Suspicious URL Domain Patterns ──
        suspicious_domain_patterns = [
            r'\d{5,}\.com',
            r'\d{4,}[a-z]+\.com',
        ]
        for url in urls:
            domain = re.sub(r'^https?://(www\.)?', '', url.lower()).split('/')[0]
            for pattern in suspicious_domain_patterns:
                if re.search(pattern, domain):
                    score += 20
                    explanation["url_issues"].append(
                        f"Numeric-heavy domain '{domain}' — common in scam URLs"
                    )
                    break

        # ── 9. URL Count ──
        if len(urls) > 3:
            score += 10
            explanation["url_issues"].append(f"Excessive URLs ({len(urls)} links found)")

        # ── 10. PhishTank & IP URLs ──
        for original_url in urls:
            url = self._unshorten_url(original_url)
            if self._check_phishtank(url):
                score += 50
                explanation["url_issues"].append("URL found in PhishTank database")
                break
            if re.search(ip_pattern, url):
                score += 40
                explanation["url_issues"].append("URL contains raw IP address")
                break

        # ── 11. ML Classification ──
        combined_text = f"Subject: {subject}\n{text_content}"
        ml_result = self._ml_predict(combined_text)
        if ml_result:
            if ml_result["is_spam"] and ml_result["confidence"] >= 0.7:
                ml_score = int(ml_result["confidence"] * 30)
                score += ml_score
                explanation["ml_analysis"].append(
                    f"ML model flagged as phishing ({ml_result['confidence']*100:.1f}% confidence)"
                )
            elif not ml_result["is_spam"] and ml_result["confidence"] < 0.3:
                explanation["ml_analysis"].append(
                    f"ML model considers legitimate ({(1 - ml_result['confidence'])*100:.1f}% confidence)"
                )
            else:
                explanation["ml_analysis"].append(
                    f"ML model uncertain ({ml_result['confidence']*100:.1f}% spam probability)"
                )

        # ── 12. Legitimate Brand Trust ──
        display_name, email_addr = email.utils.parseaddr(sender)
        sender_domain = email_addr.split('@')[-1].lower() if email_addr and '@' in email_addr else ""
        high_profile_domains = ['paypal.com', 'apple.com', 'microsoft.com', 'google.com', 'amazon.com', 'chase.com', 'netflix.com']
        if sender_domain in high_profile_domains:
            all_links_match = True
            for original_url in urls:
                clean_url = original_url.lower()
                clean_url = re.sub(r'^https?://(www\.)?', '', clean_url)
                link_domain = clean_url.split('/')[0]
                if not (link_domain == sender_domain or link_domain.endswith('.' + sender_domain)):
                    all_links_match = False
                    break
            if all_links_match:
                score -= 40
                explanation["brand_trust"].append(
                    f"Legitimate brand '{sender_domain}' — all links match sender domain"
                )

        # ── Cap score ──
        score = max(0, min(score, 100))

        # ── Determine risk level ──
        if score < 30:
            level = "Low"
        elif score < 70:
            level = "Medium"
        else:
            level = "High"

        # ── Determine 3-way category ──
        # Phishing: credential harvest, spoofing, brand impersonation, PhishTank hits
        # Spam/Junk: unsolicited ads, scams, lotteries, emoji-heavy, numeric domains
        # Legitimate: trusted sender, no red flags
        phishing_signals = (
            len(explanation["spoofing"]) > 0
            or any("PhishTank" in s for s in explanation["url_issues"])
            or any("raw IP" in s.lower() for s in explanation["url_issues"])
            or any("raw IP" in s.lower() for s in explanation["suspicious_sender"])
            or any("password" in s.lower() or "suspend" in s.lower() or "account closure" in s.lower()
                   for s in explanation["urgency"])
        )
        # Separate strong spam signals from weak content flags
        strong_spam_signals = (
            len(explanation["scam_keywords"]) > 0
            or any("numeric-heavy" in s.lower() for s in explanation["url_issues"])
        )
        weak_content_flags_only = (
            len(explanation["content_flags"]) > 0
            and not strong_spam_signals
            and not phishing_signals
            and len(explanation["spoofing"]) == 0
            and len(explanation["suspicious_sender"]) == 0
            and len(explanation["urgency"]) == 0
            and len(explanation["url_issues"]) == 0
        )
        has_trust = len(explanation["brand_trust"]) > 0

        if score == 0 and not phishing_signals:
            category = "legitimate"
        elif phishing_signals and score >= 40:
            category = "phishing"
        elif score >= 80 and not phishing_signals:
            # High score but no classic phishing signals → spam/junk
            category = "spam_junk"
        elif score >= 70:
            category = "phishing"
        elif weak_content_flags_only and score < 40:
            # Only content flags (emoji, greeting) with modest score — likely false positive
            category = "legitimate"
        elif strong_spam_signals or score >= 30:
            category = "spam_junk"
        elif has_trust and score < 30:
            category = "legitimate"
        else:
            category = "legitimate"

        # ── Build human-readable summary ──
        summary_parts = []
        if category == "phishing":
            summary_parts.append("This email shows strong signs of a phishing attempt.")
        elif category == "spam_junk":
            summary_parts.append("This email appears to be spam or unsolicited junk.")
        else:
            summary_parts.append("This email appears to be legitimate.")

        detail_lines = []
        if explanation["spoofing"]:
            detail_lines.append(f"• Spoofing: {'; '.join(explanation['spoofing'])}")
        if explanation["suspicious_sender"]:
            detail_lines.append(f"• Suspicious sender: {'; '.join(explanation['suspicious_sender'])}")
        if explanation["urgency"]:
            detail_lines.append(f"• Urgency tactics: {', '.join(explanation['urgency'])}")
        if explanation["scam_keywords"]:
            detail_lines.append(f"• Scam indicators: {'; '.join(explanation['scam_keywords'])}")
        if explanation["url_issues"]:
            detail_lines.append(f"• URL problems: {'; '.join(explanation['url_issues'])}")
        if explanation["content_flags"]:
            detail_lines.append(f"• Content flags: {'; '.join(explanation['content_flags'])}")
        if explanation["ml_analysis"]:
            detail_lines.append(f"• ML analysis: {'; '.join(explanation['ml_analysis'])}")
        if explanation["brand_trust"]:
            detail_lines.append(f"• Trust signals: {'; '.join(explanation['brand_trust'])}")

        if detail_lines:
            summary_parts.append("What triggered this classification:")
            summary_parts.extend(detail_lines)
        else:
            summary_parts.append("No suspicious patterns were detected.")

        human_explanation = "\n".join(summary_parts)

        # Legacy pipe-delimited justification (backward compat)
        all_justifications = []
        for v in explanation.values():
            all_justifications.extend(v)
        if not all_justifications:
            all_justifications.append("No threats detected.")

        return {
            "category": category,           # "phishing" | "legitimate" | "spam_junk"
            "score_level": level,           # "Low" | "Medium" | "High"
            "numeric_score": score,         # 0-100
            "justification": " | ".join(all_justifications),
            "explanation": explanation,     # structured dict by category
            "explanation_text": human_explanation,  # human-readable paragraph
        }
