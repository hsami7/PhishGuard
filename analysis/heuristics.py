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
        self.suspicious_tlds = ['.xyz', '.top', '.click', '.club', '.ru', '.cn']
        self.urgency_keywords = ['urgent', 'immediate', 'password', 'bank', 'suspend', 'action required', 'verify', 'account closure']
        
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
        justifications = []

        sender_lower = sender.lower()
        subject_lower = subject.lower()
        body_lower = text_content.lower()

        # Advanced Spoofing Detection
        is_spoofed, spoof_justification = self._detect_spoofing(sender)
        if is_spoofed:
            score += 40
            justifications.append(spoof_justification)

        # Typosquatting Detection
        is_typosquat, typosquat_justification = self._detect_typosquatting(sender)
        if is_typosquat:
            score += 40
            justifications.append(typosquat_justification)

        # Sender Heuristics
        for tld in self.suspicious_tlds:
            if sender_lower.endswith(tld) or f"{tld}>" in sender_lower:
                score += 30
                justifications.append(f"Suspicious sender domain TLD ({tld})")
                break
        
        # Check if sender is an IP address
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        if re.search(ip_pattern, sender):
            score += 30
            justifications.append("Sender contains raw IP address")
        
        # Subject and Body Urgency Heuristics
        for keyword in self.urgency_keywords:
            if keyword in subject_lower:
                score += 20
                justifications.append(f"Urgency keyword in subject: '{keyword}'")
            if keyword in body_lower:
                score += 10
                justifications.append(f"Urgency keyword in body: '{keyword}'")

        # Generic Greeting Heuristics
        if "dear customer" in body_lower or "dear user" in body_lower:
            score += 10
            justifications.append("Generic greeting detected")

        # URL Heuristics
        if len(urls) > 3:
            score += 10
            justifications.append("Excessive number of URLs")

        for original_url in urls:
            url = self._unshorten_url(original_url)
            
            if self._check_phishtank(url):
                score += 50
                justifications.append("URL found in PhishTank database")
                break
                
            if re.search(ip_pattern, url):
                score += 40
                justifications.append("URL contains raw IP address")
                break

        # ML-based Classification
        combined_text = f"Subject: {subject}\n{text_content}"
        ml_result = self._ml_predict(combined_text)
        if ml_result:
            if ml_result["is_spam"] and ml_result["confidence"] >= 0.7:
                ml_score = int(ml_result["confidence"] * 30)
                score += ml_score
                justifications.append(
                    f"ML classifier: Phishing detected ({ml_result['confidence']*100:.1f}% confidence)"
                )
            elif not ml_result["is_spam"] and ml_result["confidence"] < 0.3:
                justifications.append(
                    f"ML classifier: Likely legitimate ({(1 - ml_result['confidence'])*100:.1f}% confidence)"
                )

        # Cap score at 100
        score = min(score, 100)

        # Determine level
        if score < 30:
            level = "Low"
        elif score < 70:
            level = "Medium"
        else:
            level = "High"

        # Ensure we always have a justification
        if not justifications:
            justifications.append("No threats detected.")

        return {
            "score_level": level,
            "numeric_score": score,
            "justification": " | ".join(justifications)
        }
