# Changelog

All notable changes to the Ghostwire theme will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-21

### Changed
- Slimmed theme repository to standard Omarchy core files consumed directly by the desktop environment.
- Moved non-standard third-party application themes, generator tools, and development assets to `ghostwire-extras`.
- Re-encoded all 14 wallpapers in `backgrounds/` to WebP capped at 4K wide (1.35 MB total, 97.4% size reduction).
- Cleaned documentation to reflect standard Omarchy theme specification.

## [1.0.0] - 2026-10-08

### Added
- Standardized Omarchy 4.x master palette in `colors.toml`.
- Expanded application color coverage and WCAG AAA compliance checks.
- Curated 14 full-resolution 2560x1440 wallpapers.

### Fixed
- Fixed stale decimal RGB in `chromium.theme` (`8,9,13` for `#08090d`).
- Calibrated palette harmony and border gradient transitions.

## [0.2.0] - 2026-10-03

### Added
- Added Omarchy 4.x Quickshell support (`shell.toml`, `shell.lock.toml`).
- Added native `keyboard.rgb`.
- Added 4 new wallpapers (fracture-core, light-weave, mainframe, prism-core).
- Enhanced `hyprlock.conf` with glitch effects and user profile layout.

## [0.1.0] - 2026-09-29

### Added
- Initial release with `colors.toml`, Waybar, Walker, SwayOSD, Mako, and 10 wallpapers.
