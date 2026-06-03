# Dark Mode Toggle Feature

## Overview

Implement a dark mode toggle that allows users to switch between light and dark themes across the Vulnerable Web Application.

## Purpose

Improve usability and accessibility by allowing users to choose a theme that matches their preference and environment.

---

## Functional Requirements

### FR-DM-1: Theme Toggle

The application SHALL provide a theme toggle button on:

* Login page
* Signup page
* Dashboard page

### FR-DM-2: Theme Switching

Users SHALL be able to switch between light and dark themes without reloading the page.

### FR-DM-3: Preference Persistence

The selected theme SHALL be stored in `localStorage` under the key `theme`. The application SHALL restore the saved theme on subsequent visits before the page renders, to prevent a flash of the wrong theme.

### FR-DM-4: System Preference Detection

When no saved preference exists in `localStorage`, the application SHALL read the user's OS preference via `prefers-color-scheme: dark` and apply it as the initial theme.

### FR-DM-5: Accessibility

The toggle button SHALL include an `aria-label` attribute that reflects the current action (e.g., "Switch to dark mode" / "Switch to light mode"). Theme color pairs SHALL maintain a minimum contrast ratio of 4.5:1 for body text against its background.

### FR-DM-6: Toggle Button Label

The toggle button SHALL display a text label or icon that reflects the currently active theme and updates immediately when the theme changes. Example: "🌙 Dark" when light is active; "☀️ Light" when dark is active.

### FR-DM-7: Theme Scope

The dark theme SHALL apply to all visible elements on each page: header, auth panels, form inputs, buttons, dashboard banner, vulnerability cards, step cards, and error messages.

### FR-DM-8: No Flash of Unstyled Content

The theme initialization script SHALL execute before the page body renders (inline `<script>` in `<head>`) to prevent a visible flash of the light theme on users who prefer dark.

---

## Non-Functional Requirements

### NFR-DM-1

The theme switch SHALL complete instantly without a page refresh or visible layout shift.

### NFR-DM-2

The selected theme SHALL remain consistent across all application pages during a session and across browser sessions.

### NFR-DM-3

The implementation SHALL use only CSS custom properties and a `data-theme` attribute on `<html>`. No JavaScript framework or external library is required.

### NFR-DM-4

The toggle SHALL be keyboard accessible (focusable, activatable via Enter/Space).

---

## Affected Files

* `frontend/static/css/styles.css` — CSS custom properties for both themes; `[data-theme="dark"]` overrides; toggle button styles
* `frontend/templates/login.html` — theme init script in `<head>`; toggle button in header
* `frontend/templates/signup.html` — theme init script in `<head>`; toggle button in header
* `frontend/templates/dashboard.html` — theme init script in `<head>`; toggle button in header

---

## Success Paths

### SP-DM-01: First Visit, No System Preference

User visits the app with no saved preference and no OS dark mode set → light theme applied → toggle button reads "🌙 Dark".

### SP-DM-02: First Visit, OS Dark Mode Enabled

User visits the app with no saved preference but OS dark mode active → dark theme applied automatically → toggle button reads "☀️ Light".

### SP-DM-03: User Toggles Theme

User clicks the toggle button on any page → theme switches instantly → button label updates → new preference saved to `localStorage`.

### SP-DM-04: Theme Persists Across Pages

User sets dark mode on the login page → navigates to signup or dashboard → dark theme is already active on load with no flash.

### SP-DM-05: Theme Persists Across Sessions

User sets dark mode, closes the browser, reopens the app → dark theme applied on first render because `localStorage` value is read in `<head>`.

---

## Edge Cases

### EC-DM-01: localStorage Unavailable

The browser blocks `localStorage` access (e.g., private browsing with strict settings, or storage quota exceeded). The theme initialization SHALL catch the exception and fall back to the OS preference or light theme. No JavaScript error SHALL propagate to the console.

### EC-DM-02: Unrecognized localStorage Value

The `theme` key in `localStorage` contains an unexpected value (e.g., `"blue"` from a third-party script). The initialization SHALL treat any value other than `"dark"` as light theme and apply the default.

### EC-DM-03: OS Preference Changes After Page Load

The user switches OS dark mode while the app is open in a tab. The existing page does not need to react — the new preference will be detected on the next page load or navigation.

### EC-DM-04: Toggle Clicked Rapidly

The user clicks the toggle button multiple times in quick succession. Each click SHALL apply the correct opposite theme with no intermediate broken state. The final `localStorage` value SHALL match the final visible theme.

### EC-DM-05: Page with Inline Error Messages

The signup page displays a password-mismatch error or the login page shows an auth error. Both error elements SHALL be visible with sufficient contrast in both light and dark themes.

### EC-DM-06: Dashboard `{{username}}` Contains HTML Characters

A username with special characters (e.g., `O'Brien`) is substituted into the dashboard. This is unrelated to theming but the dark theme styles SHALL not interfere with any inline-substituted content.

---

## Acceptance Criteria

### AC-DM-01

Given a user with no saved preference and no OS dark mode, when any page loads, then the light theme SHALL be active and the toggle button SHALL be visible on the page.

### AC-DM-02

Given a user with OS dark mode enabled and no saved preference, when any page loads, then the dark theme SHALL be applied before the page is visible (no flash of light theme).

### AC-DM-03

Given the light theme is active, when the user clicks the toggle, then the dark theme SHALL be applied instantly without a page reload, the button label SHALL update, and `localStorage.getItem('theme')` SHALL equal `"dark"`.

### AC-DM-04

Given the dark theme is saved in `localStorage`, when the user navigates to a different page, then the dark theme SHALL be active on that page from the first render with no visible flash.

### AC-DM-05

Given the dark theme is active, when the user closes and reopens the browser, then the dark theme SHALL be restored on the first page visited.

### AC-DM-06

Given `localStorage` throws an exception, when the page loads, then the application SHALL render in the fallback theme without a JavaScript error.

### AC-DM-07

Given the toggle button is focused via keyboard (Tab), when the user presses Enter or Space, then the theme SHALL switch identically to a mouse click.

---

## Test Cases

| ID | Scenario | Precondition | Expected Result |
|----|----------|--------------|-----------------|
| TC-DM-01 | First visit, no preference, no OS dark mode | `localStorage` empty, OS light | Light theme active; toggle shows "🌙 Dark" |
| TC-DM-02 | First visit, OS dark mode on | `localStorage` empty, OS dark | Dark theme active on load; no flash |
| TC-DM-03 | Toggle light → dark | Light theme active | Dark theme applied instantly; button shows "☀️ Light"; `localStorage` = `"dark"` |
| TC-DM-04 | Toggle dark → light | Dark theme active | Light theme applied instantly; button shows "🌙 Dark"; `localStorage` = `"light"` |
| TC-DM-05 | Theme persists across page navigation | Dark saved in `localStorage` | Dashboard, login, signup all load in dark without flash |
| TC-DM-06 | Theme persists after browser restart | Dark saved in `localStorage` | Dark theme applied on first render of any page |
| TC-DM-07 | Toggle on login page | Any theme | Theme changes on login page correctly |
| TC-DM-08 | Toggle on signup page | Any theme | Theme changes on signup page correctly |
| TC-DM-09 | Toggle on dashboard page | Any theme | Theme changes on dashboard page correctly |
| TC-DM-10 | localStorage blocked | Simulate storage exception | Page renders in fallback theme; no JS error in console |
| TC-DM-11 | Unrecognized localStorage value | `localStorage.theme = "blue"` | Light theme applied as default |
| TC-DM-12 | Rapid toggle clicks | Light theme active | Final theme matches final click; no broken state |
| TC-DM-13 | Error message contrast in dark mode | Dark theme active; trigger auth error | Error message text legible against dark background |
| TC-DM-14 | Keyboard toggle activation | Focus toggle button via Tab | Enter/Space switches theme identically to mouse click |
| TC-DM-15 | Toggle ARIA label updates | Toggle theme | `aria-label` reflects the new action after each switch |
