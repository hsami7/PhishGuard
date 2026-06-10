import email
from email import policy
import re
from typing import Dict, Any, List

URL_REGEX = re.compile(r'(?i)\bhttps?://[^\s<>"\'{}|\\^`]+')

def preprocess_raw_email(raw_content: str) -> str:
    """
    Strips extra blank lines within the header section to handle copy-pasted raw emails.
    """
    lines = raw_content.splitlines()
    cleaned_lines = []
    header_regex = re.compile(r'^[A-Za-z0-9\-]+:')
    
    in_headers = True
    for line in lines:
        stripped = line.strip()
        if in_headers:
            if not stripped:
                continue
            
            # If line starts with header pattern or is a header continuation
            if header_regex.match(stripped) or (cleaned_lines and line.startswith((' ', '\t'))):
                cleaned_lines.append(line)
            else:
                # First non-header line transitions us out of header parsing
                in_headers = False
                cleaned_lines.append("")  # Standard single blank line boundary
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
            
    return "\n".join(cleaned_lines)

def parse_email(raw_content: str) -> Dict[str, Any]:
    """
    Parses a raw .eml string and extracts headers, body text, and links.
    Uses best-effort parsing (email.policy.default) to handle malformed emails.
    """
    cleaned_content = preprocess_raw_email(raw_content)
    # Use policy.default to handle malformed emails gracefully
    msg = email.message_from_string(cleaned_content, policy=policy.default)
    
    # 1. Header Extraction
    headers = {
        "To": msg.get("To", ""),
        "From": msg.get("From", ""),
        "Subject": msg.get("Subject", ""),
        "Date": msg.get("Date", ""),
        "Return-Path": msg.get("Return-Path", "")
    }
    
    # Clean up None values (get() might return None if header exists but is empty)
    for k, v in headers.items():
        if v is None:
            headers[k] = ""
    
    # 2. Body Extraction & Decoding
    body_text_parts = []
    
    if msg.is_multipart():
        for part in msg.walk():
            # Skip multipart containers
            if part.is_multipart():
                continue
                
            content_type = part.get_content_type()
            # We want both text/plain and text/html
            if content_type in ["text/plain", "text/html"]:
                payload = part.get_payload(decode=True)
                if payload:
                    try:
                        # Attempt to decode bytes to string using the specified charset
                        charset = part.get_content_charset() or 'utf-8'
                        text = payload.decode(charset, errors='replace')
                        body_text_parts.append(text)
                    except Exception:
                        # Fallback if decoding fails completely
                        body_text_parts.append(payload.decode('utf-8', errors='replace'))
    else:
        # Not multipart, just get the payload
        content_type = msg.get_content_type()
        # If no content type is specified, assume text/plain
        if content_type in ["text/plain", "text/html"] or not msg.get("Content-Type"):
            payload = msg.get_payload(decode=True)
            if payload:
                try:
                    charset = msg.get_content_charset() or 'utf-8'
                    text = payload.decode(charset, errors='replace')
                    body_text_parts.append(text)
                except Exception:
                    body_text_parts.append(payload.decode('utf-8', errors='replace'))
    
    # Concatenate all collected text parts
    full_body_text = "\n".join(body_text_parts)
    
    # 3. URL Regex Harvesting
    extracted_urls = URL_REGEX.findall(full_body_text)
    # Deduplicate while preserving order
    urls = list(dict.fromkeys(extracted_urls))
    
    return {
        "headers": headers,
        "body_text": full_body_text,
        "urls": urls
    }
