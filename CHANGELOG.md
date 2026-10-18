# Changelog

All notable changes to the Ghostwire theme will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-08

### Added
- **Single-Source Palette Generator**:
  - `scripts/generate.py`: Automatically generates and synchronizes 29+ palette-dependent configs from `colors.toml`.
  - `scripts/check.sh` and `--check` CLI flag: CI-style synchronization and syntax validation verifying zero configuration drift.
- **Complete Telegram Theme Suite (`telegram/`)**:
  - `ghostwire.tdesktop-theme`: Native package containing `colors.tdesktop-theme` and `background.jpg` (sub-500KB low-contrast artwork).
  - Full override mapping: cyan accents, deep teal-tinted outgoing bubbles (`#0f1c20`), lighter incoming bubbles (`#151b26`), purple highlights, cyan unread badges with dark text (`#06070c`).
  - `ghostwire.attheme`: Android Telegram theme.
  - `ghostwire-material.attheme`: Material / Telegram-X variant with purple header and cyan FAB.
  - `scripts/contrast_check.py`: WCAG 2.1 AAA compliance auditor verifying **11.4:1** contrast on message bubbles and **11.9:1** on unread badges.
  - `telegram/README.md`: Step-by-step installation instructions including Flatpak and Snap sandbox path caveats.
  - `telegram/build.sh`: Automated bundle packager.
- **Expanded Application Ecosystem**:
  - Added support for `lazygit` (`lazygit.yml`).
  - Added support for `yazi` (`yazi.toml`).
  - Added support for `tmux` (`tmux.conf`).
  - Added support for `wezterm` (`wezterm.lua`).
  - Added support for `obsidian` (`obsidian.css`).
  - Added support for `spicetify` (`spicetify/color.ini`).
- **Visuals & Documentation**:
  - Wallpaper collection preview montage (`screenshots/wallpapers-montage.png`) showcasing all 14 2560x1440 backgrounds.
  - Added Telegram Desktop mock screenshot (`screenshots/telegram.png`).
  - Updated README with status badges, one-line installation, and exhaustive 29-application support matrix.
  - Created `AUDIT.md` comprehensive repository audit report.

### Fixed
- Fixed stale decimal RGB in `chromium.theme` (`13,17,23` from stale `#0d1117`, corrected to `8,9,13` for `#08090d`).
- Fixed typo in `zed.json` (`#1a2333ff` &rarr; `#1a2233ff`).
- Fixed off-palette colors in `vencord.theme.css` (`#9aa8c2`, `#a3aec4`).
- Fixed off-palette colors in `vscode-theme` (`#182031`, `#1a2536`, `#1a2130`, `#23304780`, `#7a8aa8`, `#9aa8c2`).

## [0.2.0] - 2026-10-03

### Added
- Added Omarchy 4.x Quickshell support (`shell.toml`, `shell.lock.toml`).
- Added native `hyprland.lua` and `keyboard.rgb`.
- Added 4 new AI wallpapers (fracture-core, light-weave, mainframe, prism-core).
- Hand-drawn block logo in `fastfetch.jsonc` and `ghostwire-ascii.txt`.
- Enhanced `hyprlock.conf` with glitch effects and user profile layout.

## [0.1.0] - 2026-09-29

### Added
- Initial release with `colors.toml`, Alacritty, Kitty, Ghostty, GTK4, Waybar, Walker, SwayOSD, Mako, and 10 wallpapers.
