# Dark Mode Toggle Implementation Plan

## Phase 1: Styling (`styles.css`)

1. Extract all current colour literals into CSS custom properties on `:root` (light theme defaults):
   ```css
   :root {
     --color-bg-body:        #eef1f8;
     --color-bg-surface:     #ffffff;
     --color-bg-header:      #ffffff;
     --color-bg-input:       #f8f9ff;
     --color-bg-panel:       linear-gradient(160deg, #0d1b5e 0%, #1a237e 45%, #283593 100%);
     --color-bg-banner:      linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
     --color-bg-step:        #1a237e;
     --color-border:         #dde3f0;
     --color-text-primary:   #1e293b;
     --color-text-secondary: #475569;
     --color-text-muted:     #64748b;
     --color-text-header:    #1a237e;
     --color-label:          #3949ab;
     --color-input-border:   #c5cae9;
   }
   ```

2. Define `[data-theme="dark"]` overrides on `html`:
   ```css
   [data-theme="dark"] {
     --color-bg-body:        #0f172a;
     --color-bg-surface:     #1e293b;
     --color-bg-header:      #1e293b;
     --color-bg-input:       #0f172a;
     --color-border:         #334155;
     --color-text-primary:   #e2e8f0;
     --color-text-secondary: #94a3b8;
     --color-text-muted:     #64748b;
     --color-text-header:    #a5b4fc;
     --color-label:          #818cf8;
     --color-input-border:   #475569;
   }
   ```

3. Replace all hardcoded colour values throughout the existing CSS rules with `var(--color-*)` references.

4. Add toggle button styles:
   ```css
   .theme-toggle {
     background: transparent;
     border: 1.5px solid var(--color-input-border);
     border-radius: 20px;
     color: var(--color-text-primary);
     cursor: pointer;
     font-size: 0.8rem;
     font-weight: 600;
     padding: 0.3rem 0.85rem;
     transition: background 0.2s, color 0.2s;
   }
   .theme-toggle:hover {
     background: var(--color-bg-input);
   }
   ```

---

## Phase 2: UI Integration (all three templates)

For each of `login.html`, `signup.html`, and `dashboard.html`:

1. Add the theme init script as the **first child of `<head>`** (before the stylesheet link) to prevent a flash of the wrong theme:
   ```html
   <script>
     (function() {
       try {
         var saved = localStorage.getItem('theme');
         var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
         var theme = saved === 'dark' || saved === 'light' ? saved : (prefersDark ? 'dark' : 'light');
         document.documentElement.setAttribute('data-theme', theme);
       } catch(e) {}
     })();
   </script>
   ```

2. Add the toggle button inside `.page-header`, between the title and the logos:
   ```html
   <button class="theme-toggle" id="theme-toggle" aria-label="Switch to dark mode">🌙 Dark</button>
   ```

3. Add the toggle management script at the bottom of `<body>`:
   ```html
   <script>
     (function() {
       var btn = document.getElementById('theme-toggle');
       function applyTheme(theme) {
         document.documentElement.setAttribute('data-theme', theme);
         try { localStorage.setItem('theme', theme); } catch(e) {}
         btn.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
         btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
       }
       // Sync button label to current theme on load
       applyTheme(document.documentElement.getAttribute('data-theme') || 'light');
       btn.addEventListener('click', function() {
         var current = document.documentElement.getAttribute('data-theme');
         applyTheme(current === 'dark' ? 'light' : 'dark');
       });
     })();
   </script>
   ```

---

## Phase 3: Verification

### Light Theme Verification

* Clear `localStorage`. Open each page (login, signup, dashboard).
* Confirm background, text, cards, header, inputs, and buttons all match the original light palette.
* Confirm toggle button is visible and reads "🌙 Dark".

### Dark Theme Verification

* Toggle to dark on each page.
* Confirm all backgrounds switch to dark values; text remains legible.
* Confirm header, auth panel, form inputs, dashboard cards, and step cards all render correctly.
* Confirm toggle button reads "☀️ Light".

### Persistence Verification

* Set dark mode on the login page → navigate to signup → confirm dark is already active.
* Set dark mode → close tab → reopen app → confirm dark loads with no flash.
* Set `localStorage.theme = "blue"` manually → reload → confirm light theme applied as fallback.

### No-Flash Verification

* Set dark mode in `localStorage` → hard-reload the dashboard → confirm page renders dark immediately with no white flash.

### Accessibility Verification

* Tab to the toggle button on each page → confirm it receives focus and is visually indicated.
* Press Enter and Space → confirm theme switches on both keys.
* Inspect `aria-label` after each toggle → confirm it updates correctly.
* Run a contrast check on dark-theme body text (`#e2e8f0`) against the dark background (`#0f172a`) — must pass 4.5:1.

### Error State Verification

* On login page in dark mode, submit wrong credentials → confirm the red error box is legible against the dark form panel.
* On signup page in dark mode, enter mismatched passwords → confirm the field error text is legible.

---

## Completion Criteria

* Theme toggle button present and functional on login, signup, and dashboard pages.
* Theme switches instantly on click with no page reload.
* Button label and `aria-label` update correctly after each toggle.
* Theme initializes from `localStorage` before first paint — no flash of wrong theme.
* OS `prefers-color-scheme` is respected when no saved preference exists.
* `localStorage` failures are silently caught — page renders in fallback theme with no JS errors.
* All colour values in `styles.css` use CSS custom properties.
* All verification tests pass.
