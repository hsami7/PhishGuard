# Phase 5: Frontend UI & Templates - Validation Strategy

## Dimensions

1. **Aesthetics & Responsiveness**: Verify the dark mode cyber theme is applied correctly, looks premium, and adapts to mobile devices.
2. **Auth Flow Integration**: Verify that users can register, log in, and that the JWT is correctly saved to the browser's `localStorage`.
3. **Application Flow**: Verify that the dashboard form successfully submits data to the API Gateway and visualizes the results.

## Release Criteria

- [ ] Navigating to `/` displays a premium, dark-themed landing page.
- [ ] Submitting the registration form creates a user and redirects to login.
- [ ] Submitting the login form saves the token and redirects to `/dashboard`.
- [ ] In the dashboard, pasting a malicious email string and clicking "Analyze" dynamically shows a Red/High Risk warning card with justifications.
