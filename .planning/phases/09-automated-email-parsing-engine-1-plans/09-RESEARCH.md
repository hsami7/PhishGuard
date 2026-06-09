# Research: Phase 09 - Automated Email Parsing Engine

## Objective
Determine how to implement best-effort email parsing, header extraction, and strict link harvesting using Python's standard libraries, based on Phase 9 requirements.

## Findings

### 1. Parsing Raw `.eml`
Python's standard library `email` module (specifically `email.parser.BytesParser` and `email.message_from_string`) is extremely robust. For "best-effort" parsing of malformed emails, we should use `email.policy.default` which attempts to gracefully handle defects (missing boundaries, bad headers) without throwing fatal exceptions.

### 2. Header Extraction
Headers like `To`, `From`, `Subject`, `Date`, and `Return-Path` can be accessed as dictionary keys on the `email.message.EmailMessage` object. They automatically handle basic decoding of RFC 2047 encoded words (e.g. `=?utf-8?q?...?=`).

### 3. Body Extraction (Multipart & Decoding)
Emails can be simple or multipart (nested). We need a recursive function to walk the parts using `msg.walk()`.
- **Decoding:** Calling `part.get_payload(decode=True)` automatically handles Base64 and Quoted-Printable decoding.
- **Preference:** We must extract text from both `text/plain` and `text/html` parts to merge the links later.

### 4. Link Harvesting (Regex)
Requirement: Strict fully qualified URLs (`http://` or `https://`).
Regex pattern: `r'(?i)\bhttps?://[^\s<>"\'{}|\\^`]+'`
This pattern:
- Is case-insensitive for the scheme (`(?i)`).
- Matches `http://` or `https://`.
- Continues until it hits whitespace or common HTML/formatting characters that aren't valid in URLs.
- Note: Beautiful Soup could be used to extract `href` attributes from HTML, but a robust regex on the raw decoded payload is often sufficient and faster for plain text + HTML merging, especially for malformed spam where `href` attributes might be intentionally broken but the link text remains.

## Validation Architecture
- **Unit Tests**: Create test cases with valid and intentionally malformed `.eml` strings.
- **Mocking**: Not strictly required since parsing is a pure function taking a string and returning a dict.
- **Edge Cases**: Missing headers, empty body, nested multipart, Base64 encoding.

## Conclusion
The implementation should introduce an `EmailParser` class or module in the `analysis/` directory. It will expose a single entry point `parse_email(raw_content: str) -> dict` returning the extracted headers, body texts, and a deduplicated list of URLs.
