# Research Summary: Intelligent Automation & UI-UX Pro-Max

## Stack Additions
- **Python Standard Library (`email`)**: Fully capable of parsing raw `.eml` and multipart messages. No third-party dependencies strictly required.
- **Python `re` (Regex)**: For URL extraction. Will need robust patterns to catch obfuscated links (e.g., `hXXps://`, missing schemes).
- **BeautifulSoup4 (Optional)**: If extracting links from complex HTML parts is required and regex becomes too brittle.
- **Tailwind CSS**: For Glassmorphism UI, using `bg-white/10`, `backdrop-blur-md`, and `border-white/20`.

## Feature Table Stakes
- **Automated Email Parsing**: Must handle multipart emails, extracting headers (To, From, Subject, Return-Path, Received) and body text.
- **Link Harvesting**: Must extract all unique URLs from both `text/plain` and `text/html` parts.
- **Single-field Dashboard**: A premium, frosted-glass textarea that accepts raw email source code or direct paste.

## Watch Out For
- **Encoding Issues**: Raw emails often use Quoted-Printable or Base64 encoding. The parser must decode these before running regex or heuristics.
- **HTML Parsing Complexity**: Regex on raw HTML is notoriously fragile. If emails are heavily formatted, a proper HTML parser might be needed to avoid false positives/negatives in link harvesting.
- **Performance**: Deep regex scans on large raw emails can be slow. Ensure regex patterns are optimized against catastrophic backtracking.
