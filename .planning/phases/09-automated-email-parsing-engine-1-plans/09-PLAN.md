# Plan: Phase 09 - Automated Email Parsing Engine

## Requirements
- PARSE-01: Parse raw .eml, extract headers
- PARSE-02: Decode multipart emails and extract text bodies
- PARSE-03: Regex link harvest

## Strategy
We will implement an `EmailParser` utility in the `analysis` package. This module will handle the parsing of raw `.eml` contents using Python's `email` module, prioritizing best-effort extraction. It will return a structured dictionary containing `headers`, `body_text`, and `urls`.

## Tasks

- [ ] **Task 1: Core Parsing & Header Extraction**
  - Create `analysis/parser.py`.
  - Implement `parse_email(raw_content: str) -> dict`.
  - Use `email.message_from_string(raw_content, policy=email.policy.default)`.
  - Extract `To`, `From`, `Subject`, `Date`, and `Return-Path` headers safely.

- [ ] **Task 2: Body Extraction & Decoding**
  - Implement a helper to recursively `walk()` the email payload.
  - Call `get_payload(decode=True)` on parts with content types `text/plain` and `text/html`.
  - Concatenate the extracted text into a single `body_text` string to satisfy the "Merge both" decision.

- [ ] **Task 3: URL Regex Harvesting**
  - Compile a regex pattern to extract strict URLs (`http://` and `https://` only).
  - Apply the pattern against the concatenated `body_text`.
  - Deduplicate the resulting URLs.
  - Return the final structured dictionary.

- [ ] **Task 4: Unit Testing**
  - Create `tests/test_parser.py` using `pytest`.
  - Add tests for valid `.eml` strings, malformed emails without boundaries, and base64 encoded multipart emails.

## Verification
Run `pytest tests/test_parser.py` to ensure all tests pass.
