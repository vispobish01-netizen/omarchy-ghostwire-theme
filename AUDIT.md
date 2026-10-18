# Ghostwire Theme Audit Report

**Date:** 2026-10-08  
**Repository:** [vispobish01-netizen/omarchy-ghostwire-theme](https://github.com/vispobish01-netizen/omarchy-ghostwire-theme)  
**Standard:** Omarchy 4.x Design Specifications & Brand Token Architecture

---

## 1. Inventory & Application Targets

| File | Target Application / Subsystem | Palette Alignment Status |
|---|---|---|
| `colors.toml` | Single source of truth (Omarchy master palette) | Reference standard (47 keys defined, 22 required Omarchy keys verified) |
| `colors.fish` | Fish shell syntax highlighting & pager | Aligned (`c8d2e6`, `50dcc8`, `9664dc`, etc.) |
| `fzf.fish` | fzf interactive fuzzy finder env vars | Aligned |
| `alacritty.toml` | Alacritty terminal emulator | Aligned |
| `ghostty.conf` | Ghostty terminal emulator | Aligned |
| `kitty.conf` | Kitty terminal emulator | Aligned |
| `gtk.css` | GTK 3/4 & libadwaita applications | Aligned |
| `waybar.css` | Waybar status bar | Aligned |
| `walker.css` | Walker application runner / launcher | Aligned |
| `swayosd.css` | SwayOSD volume / brightness indicators | Aligned |
| `mako.ini` | Mako notification daemon | Aligned |
| `hyprland.conf` | Hyprland classic configuration | Aligned |
| `hyprland.lua` | Hyprland Omarchy 4.x Lua theme | Aligned |
| `hyprlock.conf` | Hyprlock lock screen | Aligned |
| `shell.toml` | Omarchy Quickshell UI theme | Aligned |
| `shell.lock.toml`| Quickshell lockfile | Aligned |
| `keyboard.rgb` | Hardware RGB keyboard backlight | Aligned (`#50dcc8`) |
| `icons.theme` | Icon theme definition (`Yaru-purple-dark`) | Aligned |
| `chromium.theme` | Chromium managed browser theme | **Fixed stale RGB**: contained `13,17,23` (decimal RGB for stale `#0d1117`), corrected to `8,9,13` (`#08090d`) |
| `btop.theme` | btop system monitor | Aligned |
| `cava_theme` | Cava audio visualizer | Aligned |
| `cliamp.theme` | cliamp terminal internet radio player | Aligned |
| `fastfetch.jsonc` | Fastfetch system information tool | Aligned |
| `starship.toml` | Starship cross-shell prompt | Aligned |
| `superfile.toml`| Superfile terminal file manager | Aligned |
| `steam.css` | Steam desktop client custom styling | Aligned |
| `neovim.lua` | Neovim standalone colorscheme | Aligned |
| `firefox/userChrome.css` | Mozilla Firefox browser chrome | Aligned |
| `firefox/userContent.css`| Mozilla Firefox about / newtab pages | Aligned |
| `zen.css` | Zen browser accent styling | Aligned |
| `zed.json` | Zed editor theme | **Minor defect**: contains typo `#1a2333ff` (should be `#1a2233ff`) |
| `vencord.theme.css` | Discord (Vencord) desktop theme | **Drift**: contains off-palette `#9aa8c2` and `#a3aec4` |
| `vscode-theme/*` | Visual Studio Code extension & theme | **Drift**: contains off-palette `#182031`, `#1a2536`, `#1a2130`, `#23304780`, `#7a8aa8`, `#9aa8c2` |
| `backgrounds/*` (14 files) | Desktop wallpapers | Aligned (all 14 unique, 2560x1440, RGB non-interlaced) |
| `lock-design/*` | SDDM / QtQuick lock screen addon | Aligned |

---

## 2. Validation & Quality Checks

1. **Required Omarchy Keys**:
   - `colors.toml` was verified against Omarchy's 22 canonical keys (`accent`, `cursor`, `foreground`, `background`, `selection_foreground`, `selection_background`, and `color0`..`color15`). All 22 keys exist, plus 25 semantic extension tokens (`dark_background`, `lighter_background`, `hyprland_active_border`, `bright_*`, etc.).
2. **Syntax Validation**:
   - TOML parsing: `alacritty.toml`, `colors.toml`, `shell.lock.toml`, `shell.toml`, `starship.toml`, `superfile.toml` pass `tomllib`.
   - JSON parsing: `vscode.json`, `zed.json`, `package.json`, `ghostwire-color-theme.json` pass `json.load`.
   - JSONC parsing: `fastfetch.jsonc` validated cleanly with `fastfetch -c fastfetch.jsonc`.
   - Lua parsing: `hyprland.lua`, `neovim.lua` pass `luac -p`.
   - CSS parsing: `gtk.css`, `waybar.css`, `walker.css`, `swayosd.css`, `steam.css`, `zen.css`, `vencord.theme.css`, `firefox/*.css` pass brace balance and syntax structure.
3. **Wallpaper Asset Verification**:
   - All 14 wallpapers in `backgrounds/` have unique SHA-256 hashes.
   - All 14 images are calibrated to exact 2560x1440 resolution.
   - No orphaned or duplicate wallpaper files found.
4. **Documentation Discrepancies**:
   - `README.md` list of supported apps omitted `cava`, `cliamp`, `fastfetch`, and `starship`.
   - `screenshots/yazi-launcher.png` exists in the repository but was omitted from the README screenshot showcase.
   - Missing visual wallpaper preview montage in the README.

---

## 3. Corrective Plan

1. **Fix Hex Discrepancies**:
   - Correct `#1a2333ff` to `#1a2233ff` in `zed.json`.
   - Standardize off-palette hex values in `vencord.theme.css` and `vscode-theme/` to strictly reference the single-source palette.
2. **Phase 2 Generator (`scripts/generate.py`)**:
   - Build a Python script that reads `colors.toml` and regenerates/synchronizes every derived application config.
   - Add a strict CI verify script (`scripts/check_sync.py` / `scripts/check.sh`) to detect any configuration drift.
3. **Phase 3 Telegram Theme**:
   - Generate `telegram/colors.tdesktop-theme` from the official Telegram Desktop dark palette with full Ghostwire overrides.
   - Generate optimized `telegram/background.jpg` and bundle into `telegram/ghostwire.tdesktop-theme`.
   - Validate WCAG AA contrast compliance for text and unread badges.
4. **Phase 4 Missing Coverage & Polish**:
   - Add configurations for `yazi`, `lazygit`, `tmux`, `wezterm`, `bat`, `obsidian`.
   - Generate wallpaper preview montage and update `README.md` and `CHANGELOG.md`.
