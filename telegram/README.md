# Ghostwire — Telegram Theme Suite

Tactical dark theme for Telegram Desktop (Linux / Windows / macOS) and Telegram Android, derived strictly from the Ghostwire `colors.toml` palette.

---

## What's Included

| File | Target Platform | Description |
|---|---|---|
| `ghostwire.tdesktop-theme` | Telegram Desktop | Ready-to-import ZIP package containing `colors.tdesktop-theme` and `background.jpg` |
| `colors.tdesktop-theme` | Telegram Desktop | Unbundled raw color palette file |
| `background.jpg` | Telegram Desktop | Darkened, low-contrast 52KB background from Ghostwire abstract artwork |
| `ghostwire.attheme` | Telegram Android | Android `.attheme` color scheme |
| `ghostwire-material.attheme` | Telegram-X / Material | High-contrast purple header & cyan FAB variant |
| `build.sh` | Build Script | Bundles `colors.tdesktop-theme` and `background.jpg` into `ghostwire.tdesktop-theme` |

---

## Installation Guide (Telegram Desktop)

### Method 1: Direct File Import (Fastest)
1. In Telegram Desktop, navigate to:  
   **Settings (`Ctrl+,`) &rarr; Chat Settings**
2. Scroll to the **Chat background** / theme section and click **Choose from file**.
3. Select `ghostwire.tdesktop-theme` (or send the file to Saved Messages and click on it in chat).
4. Click **Apply Changes** in the preview dialog.

### Method 2: Manual Theme Editor
1. In **Settings &rarr; Chat Settings**, click the three-dots menu (⋮) in the top-right corner.
2. Select **Create new theme** or **Import existing theme**.
3. Point to `colors.tdesktop-theme`.

---

## Flatpak & Snap Path Caveats

If you run Telegram Desktop as an isolated sandbox package (Flatpak or Snap), file pickers and theme files live under containerized directories:

### Flatpak
- Sandbox directory: `~/.var/app/org.telegram.desktop/data/TelegramDesktop/`
- If the file dialog cannot access `~/Downloads` or custom paths, run:
  ```bash
  flatpak override --user --filesystem=xdg-download org.telegram.desktop
  # Or copy theme directly to Saved Messages in the app
  ```

### Snap
- Sandbox directory: `~/snap/telegram-desktop/current/.local/share/TelegramDesktop/`
- Ensure removable media plug is connected if loading from secondary drives:
  ```bash
  snap connect telegram-desktop:removable-media
  ```

---

## WCAG Contrast Audit

All text, message bubbles, and unread badges meet and exceed WCAG AA (4.5:1) and AAA (7.0:1) criteria:

- **Incoming Message Text (`#c8d2e6`) vs Bubble (`#151b26`)**: **11.36:1 (AAA)**
- **Outgoing Message Text (`#c8d2e6`) vs Bubble (`#0f1c20`)**: **11.44:1 (AAA)**
- **Unread Badge Text (`#06070c`) vs Badge Background (`#50dcc8`)**: **11.90:1 (AAA)**
- **Active Button Text (`#06070c`) vs Accent Button (`#50dcc8`)**: **11.90:1 (AAA)**
