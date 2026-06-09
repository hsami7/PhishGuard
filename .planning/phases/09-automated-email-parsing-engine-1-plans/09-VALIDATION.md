# Validation Strategy: Phase 09

## 1. Unit Tests
- Test valid `.eml` extraction for headers and URLs.
- Test malformed `.eml` (missing boundaries) to ensure best-effort extraction works without crashing.
- Test multipart decoding for Base64 and Quoted-Printable.
- Test URL regex for strict `http/https` extraction and deduplication.

## 2. Integration Tests
- Verify that `parse_email` can process inputs without throwing exceptions.

## 3. Manual UAT
- Paste a complex `.eml` string into the console/REPL to verify output format.
