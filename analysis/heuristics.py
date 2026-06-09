import re
import requests
import sqlite3
import email.utils

class EmailAnalyzer:
    def __init__(self):
        self.suspicious_tlds = ['.xyz', '.top', '.click', '.club', '.ru', '.cn']
        self.urgency_keywords = ['urgent', 'immediate', 'password', 'bank', 'suspend', 'action required', 'verify', 'account closure']
    
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
