# Requirements: Milestone v2.0

## Active Requirements

### Email Parsing & Extraction
- [ ] **PARSE-01**: The system accepts and parses raw `.eml` or source code format, automatically extracting headers (To, From, Subject, Date, Return-Path).
- [ ] **PARSE-02**: The system automatically decodes multipart emails (Base64/Quoted-Printable) and extracts text bodies.
- [ ] **PARSE-03**: The system uses robust regex to harvest all unique URLs from both plain text and HTML bodies.

### UI & Dashboard
- [ ] **UI-04**: The dashboard provides a single, premium glassmorphism-styled text area for raw email submission instead of separate metadata fields.
- [ ] **UI-05**: The dashboard displays the extracted links and parsed headers alongside the analysis score.

## Future Requirements (Deferred)
(None)

## Out of Scope
- Full `.eml` file upload support (drag and drop files) is excluded to keep the backend lightweight. Users must paste the raw text source code into the single-field dashboard.

## Traceability
| REQ-ID | Phase | Status |
|--------|-------|--------|
| PARSE-01 | Phase 9 | Pending |
| PARSE-02 | Phase 9 | Pending |
| PARSE-03 | Phase 9 | Pending |
| UI-04 | Phase 10 | Pending |
| UI-05 | Phase 10 | Pending |
