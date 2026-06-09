import re

class EmailAnalyzer:
    def __init__(self):
        self.suspicious_tlds = ['.xyz', '.top', '.click', '.club', '.ru', '.cn']
        self.urgency_keywords = ['urgent', 'immediate', 'password', 'bank', 'suspend', 'action required', 'verify', 'account closure']
    
    def analyze(self, sender: str, subject: str, text_content: str, urls: list[str]):
        score = 0
        justifications = []

        sender_lower = sender.lower()
        subject_lower = subject.lower()
        body_lower = text_content.lower()

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

        for url in urls:
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
