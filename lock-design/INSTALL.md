# Ghostwire Lock Design — Install (Omarchy 4 / Quattro)

Quattro's stock lock screen is a single fixed layout with no plugin hook for
custom designs, so a full glitch-clock replica needs a third-party
lock-service plugin: **Lock Screen Explorer** by SirJul1337. It replaces the
built-in `omarchy.lock` service with a picker that supports custom `.qml`
designs, and it inherits colors/fonts from your active Omarchy theme
automatically.

## 1. Install & enable the plugin

```bash
omarchy plugin add https://github.com/SirJul1337/omarchy-lock-explorer.git --enable
omarchy restart shell
```

This takes over the `lock` IPC target from the stock service — Super+L (or
however you trigger lock) now opens the explorer's lock screen.

## 2. Drop in the Ghostwire design

```bash
mkdir -p ~/.config/omarchy/lock-designs
cp Ghostwire.qml ~/.config/omarchy/lock-designs/
omarchy-shell lock rescanDesigns
```

## 3. Select it

Open the lock screen explorer (however your keybind opens it, or via the
Omarchy menu), find **Ghostwire** under *Custom*, and select it. Or set it
directly:

```bash
omarchy-shell lock setDesign ghostwire
```

## Notes / caveats

- This QML file was written against the **documented** DesignBase contract in
  the plugin's README (properties: `passwordText`, `failureMessage`,
  `failedAttempts`, `authenticatingPassword`, `fingerprintConfigured`,
  `inputEnabled`, `now`, `userName`, `hostName`, `greeting()`), not tested
  against a live Quattro shell. If it fails to load:
  ```bash
  omarchy plugin validate ~/.config/omarchy/plugins/io.github.sirjul1337.lock-explorer
  qs log -p "$OMARCHY_PATH/shell" --tail 100
  ```
  and compare against one of the plugin's own shipped designs (e.g. `Zen.qml`,
  copyable via `omarchy-shell lock customize zen`) for the exact current API —
  property names have moved before between plugin versions.
- Glitch layers use `Timer`-driven random visibility instead of shell
  scripting (the old `cmd[update:N]` hyprlock trick), since Quickshell designs
  are plain QML/JS, not shell commands.
- Wallpaper blur comes from the design's own `Wallpaper { blurred: true }`,
  independent of your theme's `colors.toml` blur settings.
