#!/usr/bin/env python3
"""
Ghostwire Theme Single-Source Palette Generator
Reads colors.toml and regenerates all palette-dependent application configs.

Usage:
    python3 scripts/generate.py          # Regenerate and write all files
    python3 scripts/generate.py --check  # Verify that all files are up to date (CI check)
"""

import sys
import os
import argparse
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_palette(colors_toml_path: Path) -> dict:
    with open(colors_toml_path, "rb") as f:
        raw = tomllib.load(f)

    # Base & surface tokens
    bg = raw.get("background", "#08090d")
    dark_bg = raw.get("dark_background", "#090c11")
    darker_bg = raw.get("darker_background", "#06070c")
    lighter_bg = raw.get("lighter_background", "#151b26")

    fg = raw.get("foreground", "#c8d2e6")
    dark_fg = raw.get("dark_foreground", "#3a4250")
    light_fg = raw.get("light_foreground", "#d8e1f2")
    bright_fg = raw.get("bright_foreground", "#e8f7f4")

    accent = raw.get("accent", "#50dcc8")
    cursor = raw.get("cursor", accent)
    selection = raw.get("selection", "#1c2740")
    selection_fg = raw.get("selection_foreground", fg)
    selection_bg = raw.get("selection_background", selection)
    muted = raw.get("muted", dark_fg)

    # Core semantic colors
    red = raw.get("red", "#dc5050")
    yellow = raw.get("yellow", "#dcb43c")
    orange = raw.get("orange", "#d9792f")
    green = raw.get("green", "#50c878")
    cyan = raw.get("cyan", accent)
    blue = raw.get("blue", "#3fc4de")
    magenta = raw.get("magenta", "#9664dc")
    brown = raw.get("brown", "#6e5a1e")

    # Bright variants
    bright_red = raw.get("bright_red", "#ec6a88")
    bright_yellow = raw.get("bright_yellow", "#fab795")
    bright_green = raw.get("bright_green", "#7ee8a8")
    bright_cyan = raw.get("bright_cyan", "#6be4e6")
    bright_blue = raw.get("bright_blue", "#6fb0e8")
    bright_magenta = raw.get("bright_magenta", "#b98ae8")

    # ANSI 0-15
    ansi = {f"color{i}": raw.get(f"color{i}", bg if i == 0 else fg) for i in range(16)}

    # Brand identity tokens
    border = "#1a2233"
    dim = muted

    return {
        "raw": raw,
        "bg": bg,
        "dark_bg": dark_bg,
        "darker_bg": darker_bg,
        "lighter_bg": lighter_bg,
        "fg": fg,
        "dark_fg": dark_fg,
        "light_fg": light_fg,
        "bright_fg": bright_fg,
        "accent": accent,
        "cursor": cursor,
        "selection": selection,
        "selection_fg": selection_fg,
        "selection_bg": selection_bg,
        "muted": muted,
        "dim": dim,
        "border": border,
        "red": red,
        "yellow": yellow,
        "orange": orange,
        "green": green,
        "cyan": cyan,
        "blue": blue,
        "magenta": magenta,
        "purple": magenta,
        "brown": brown,
        "bright_red": bright_red,
        "bright_yellow": bright_yellow,
        "bright_green": bright_green,
        "bright_cyan": bright_cyan,
        "bright_blue": bright_blue,
        "bright_magenta": bright_magenta,
        **ansi,
        # Helper conversions (strip '#')
        "h_bg": bg.lstrip("#"),
        "h_dark_bg": dark_bg.lstrip("#"),
        "h_darker_bg": darker_bg.lstrip("#"),
        "h_lighter_bg": lighter_bg.lstrip("#"),
        "h_fg": fg.lstrip("#"),
        "h_dark_fg": dark_fg.lstrip("#"),
        "h_light_fg": light_fg.lstrip("#"),
        "h_bright_fg": bright_fg.lstrip("#"),
        "h_accent": accent.lstrip("#"),
        "h_selection": selection.lstrip("#"),
        "h_border": border.lstrip("#"),
        "h_red": red.lstrip("#"),
        "h_yellow": yellow.lstrip("#"),
        "h_green": green.lstrip("#"),
        "h_blue": blue.lstrip("#"),
        "h_magenta": magenta.lstrip("#"),
        "h_purple": magenta.lstrip("#"),
    }

def gen_gtk_css(p: dict) -> str:
    return f"""/* Ghostwire — GTK4 / libadwaita override
 * Omarchy's colors.toml templates terminal/Hyprland/Waybar/btop/etc, but
 * NOT GTK apps (Nautilus, Text Editor, Settings, and other libadwaita apps).
 * Drop this in as gtk.css and Omarchy will symlink it into
 * ~/.config/gtk-4.0/gtk.css (and gtk-3.0/gtk.css) when the theme is active.
 */

@define-color accent_color        {p['accent']};
@define-color accent_bg_color     {p['accent']};
@define-color accent_fg_color     {p['darker_bg']};

@define-color window_bg_color     {p['bg']};
@define-color window_fg_color     {p['fg']};
@define-color view_bg_color       {p['dark_bg']};
@define-color view_fg_color       {p['fg']};

@define-color headerbar_bg_color  {p['dark_bg']};
@define-color headerbar_fg_color  {p['fg']};
@define-color headerbar_border_color {p['border']};
@define-color headerbar_backdrop_color {p['darker_bg']};
@define-color headerbar_shade_color rgba(0, 0, 0, 0.25);

@define-color sidebar_bg_color    {p['darker_bg']};
@define-color sidebar_fg_color    {p['fg']};
@define-color sidebar_backdrop_color {p['darker_bg']};

@define-color card_bg_color       {p['lighter_bg']};
@define-color card_fg_color       {p['fg']};
@define-color card_shade_color    rgba(0, 0, 0, 0.25);

@define-color dialog_bg_color     {p['bg']};
@define-color dialog_fg_color     {p['fg']};

@define-color popover_bg_color    {p['dark_bg']};
@define-color popover_fg_color    {p['fg']};

@define-color shade_color         rgba(0, 0, 0, 0.25);
@define-color scrollbar_outline_color rgba(0, 0, 0, 0.5);

@define-color destructive_bg_color {p['red']};
@define-color destructive_fg_color {p['darker_bg']};
@define-color success_bg_color    {p['green']};
@define-color success_fg_color    {p['darker_bg']};
@define-color warning_bg_color    {p['yellow']};
@define-color warning_fg_color    {p['darker_bg']};
@define-color error_bg_color      {p['red']};
@define-color error_fg_color      {p['darker_bg']};

/* selection / cursor accents */
selection,
*:selected {{
    background-color: {p['selection']};
    color: {p['bright_fg']};
}}

/* thin cyan focus ring instead of GTK's default blue */
*:focus-visible {{
    outline-color: {p['accent']};
}}

/* subtle purple tint on active/checked toggles, matching the QML lock design */
switch:checked,
checkbutton check:checked,
radiobutton radio:checked {{
    background-color: {p['magenta']};
}}
"""

def gen_waybar_css(p: dict) -> str:
    return f"""/* Ghostwire — Waybar style
 * Omarchy auto-generates waybar colors from colors.toml; this hand file adds
 * the extra polish (rounded modules, cyan/purple split, glow on hover) that
 * a plain color substitution doesn't give you.
 */

* {{
    font-family: "JetBrainsMono Nerd Font", monospace;
    font-size: 13px;
    border: none;
    border-radius: 0;
    min-height: 0;
}}

window#waybar {{
    background-color: {p['bg']};
    color: {p['fg']};
    border-bottom: 1px solid {p['border']};
}}

#workspaces {{
    background-color: {p['dark_bg']};
    border-radius: 8px;
    margin: 4px 4px;
    padding: 0 4px;
}}

#workspaces button {{
    color: {p['dark_fg']};
    padding: 0 8px;
    border-radius: 6px;
}}

#workspaces button.active {{
    color: {p['darker_bg']};
    background-color: {p['accent']};
}}

#workspaces button.urgent {{
    color: {p['darker_bg']};
    background-color: {p['red']};
}}

#workspaces button:hover {{
    background-color: {p['selection']};
    color: {p['bright_fg']};
}}

#clock,
#battery,
#cpu,
#memory,
#temperature,
#network,
#pulseaudio,
#tray,
#custom-notification,
#backlight,
#bluetooth {{
    background-color: {p['dark_bg']};
    color: {p['fg']};
    padding: 0 10px;
    margin: 4px 2px;
    border-radius: 8px;
}}

#clock {{
    color: {p['accent']};
    font-weight: bold;
}}

#battery.charging {{
    color: {p['green']};
}}

#battery.warning:not(.charging) {{
    color: {p['yellow']};
}}

#battery.critical:not(.charging) {{
    color: {p['red']};
    animation: blink-critical 1.5s steps(2) infinite;
}}

@keyframes blink-critical {{
    to {{ color: {p['bright_fg']}; }}
}}

#network.disconnected {{
    color: {p['red']};
}}

#pulseaudio.muted {{
    color: {p['dark_fg']};
}}

#cpu {{
    color: {p['blue']};
}}

#memory {{
    color: {p['magenta']};
}}

#temperature.critical {{
    color: {p['red']};
}}

#tray > .passive {{
    -gtk-icon-effect: dim;
}}

#tray > .needs-attention {{
    -gtk-icon-effect: highlight;
    background-color: {p['red']};
}}

tooltip {{
    background-color: {p['dark_bg']};
    border: 1px solid {p['border']};
    border-radius: 8px;
}}

tooltip label {{
    color: {p['fg']};
}}
"""

def gen_walker_css(p: dict) -> str:
    return f"""/* Ghostwire — Walker (app launcher) style
 * Omarchy auto-generates Walker's colors from colors.toml; this hand file
 * adds the rounded, glass-panel look and cyan selection highlight. Selector
 * names follow Walker's default GTK4 layer-shell widget tree — if your
 * Walker version uses different IDs, check `walker --gtk-inspector` (or
 * GTK_DEBUG=interactive walker) and adjust the #ids below to match.
 */

* {{
    font-family: "JetBrainsMono Nerd Font", monospace;
    font-size: 14px;
}}

#window {{
    background-color: transparent;
}}

#box {{
    background-color: {p['bg']};
    border: 1px solid {p['border']};
    border-radius: 14px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
}}

#search {{
    background-color: {p['dark_bg']};
    border-bottom: 1px solid {p['border']};
    border-radius: 14px 14px 0 0;
    padding: 10px 14px;
}}

#input {{
    background-color: transparent;
    color: {p['bright_fg']};
    caret-color: {p['accent']};
}}

#input placeholder {{
    color: {p['dark_fg']};
}}

#icon {{
    color: {p['accent']};
}}

#list {{
    background-color: transparent;
    padding: 6px;
}}

#item {{
    border-radius: 8px;
    padding: 6px 10px;
    color: {p['fg']};
}}

#item:selected,
#item.selected {{
    background-color: {p['selection']};
    color: {p['bright_fg']};
}}

#item image,
#item .icon {{
    color: {p['blue']};
}}

#item .label {{
    color: inherit;
}}

#item .sub,
#item .sub-label {{
    color: {p['dark_fg']};
}}

#placeholder {{
    color: {p['dark_fg']};
}}

#keybinds,
#keybind {{
    color: {p['dark_fg']};
}}

#keybind-label {{
    background-color: {p['lighter_bg']};
    color: {p['magenta']};
    border-radius: 4px;
    padding: 1px 5px;
}}

scrollbar {{
    background-color: transparent;
}}

scrollbar slider {{
    background-color: {p['dark_fg']};
    border-radius: 4px;
}}
"""

def gen_mako_ini(p: dict) -> str:
    return f"""# Ghostwire — mako theme
# Omarchy auto-generates a mako config from colors.toml; this hand file adds
# per-urgency border colors and slightly larger radius/padding for the
# glass-panel look used across the rest of the theme.

background-color={p['bg']}e6
text-color={p['fg']}
border-color={p['border']}
progress-color=over {p['selection']}
border-size=1
border-radius=10
padding=10
margin=8
width=360
height=120
font=JetBrainsMono Nerd Font 11
icons=1
max-icon-size=48
default-timeout=6000
ignore-timeout=0

[urgency=low]
border-color={p['dark_fg']}
text-color={p['fg']}

[urgency=normal]
border-color={p['accent']}
text-color={p['fg']}

[urgency=high]
border-color={p['red']}
text-color={p['bright_fg']}
default-timeout=0

[category=mount]
border-color={p['green']}

[category=network]
border-color={p['blue']}
"""

def gen_swayosd_css(p: dict) -> str:
    return f"""/* Ghostwire — SwayOSD style
 * Omarchy auto-generates SwayOSD colors from colors.toml; this hand file
 * adds the rounded glass-panel look and a cyan progress fill (purple for
 * capslock, per SwayOSD's default class split).
 */

window {{
    background-color: {p['bg']};
    border: 1px solid {p['border']};
    border-radius: 16px;
    padding: 18px;
}}

#container {{
    background-color: transparent;
}}

image {{
    color: {p['fg']};
    -gtk-icon-effect: none;
}}

label {{
    color: {p['fg']};
    font-family: "JetBrainsMono Nerd Font", monospace;
    font-size: 14px;
}}

progressbar {{
    background-color: transparent;
}}

progressbar trough {{
    background-color: {p['selection']};
    border-radius: 8px;
    min-height: 10px;
}}

progressbar progress {{
    background-color: {p['accent']};
    border-radius: 8px;
    min-height: 10px;
}}

progressbar.capslock progress,
#capslock progress {{
    background-color: {p['magenta']};
}}

progressbar.muted progress,
#muted progress {{
    background-color: {p['red']};
}}
"""

def gen_cava_theme(p: dict) -> str:
    return f"""# Ghostwire — cava theme
# Append/source this into ~/.config/cava/config, or `cat` it into the
# [color] section. Bars run cyan -> blue -> purple, matching the
# teal-to-purple identity gradient used across the theme.

[color]
background = '{p['bg']}'
foreground = '{p['accent']}'
gradient = 1
gradient_count = 3
gradient_color_1 = '{p['accent']}'
gradient_color_2 = '{p['blue']}'
gradient_color_3 = '{p['magenta']}'

[general]
bar_width = 2
bar_spacing = 1
"""

def gen_alacritty_toml(p: dict) -> str:
    return f"""# Ghostwire — Alacritty explicit color config
# Merge into ~/.config/alacritty/alacritty.toml, or `import = ["~/.config/omarchy/current/theme/alacritty.toml"]`

[colors.primary]
background = "{p['bg']}"
foreground = "{p['fg']}"
dim_foreground = "{p['dark_fg']}"
bright_foreground = "{p['bright_fg']}"

[colors.cursor]
text = "{p['bg']}"
cursor = "{p['accent']}"

[colors.vi_mode_cursor]
text = "{p['bg']}"
cursor = "{p['magenta']}"

[colors.selection]
text = "{p['fg']}"
background = "{p['selection']}"

[colors.search.matches]
foreground = "{p['bg']}"
background = "{p['blue']}"

[colors.search.focused_match]
foreground = "{p['bg']}"
background = "{p['accent']}"

[colors.normal]
black = "{p['bg']}"
red = "{p['red']}"
green = "{p['green']}"
yellow = "{p['yellow']}"
blue = "{p['blue']}"
magenta = "{p['magenta']}"
cyan = "{p['cyan']}"
white = "{p['fg']}"

[colors.bright]
black = "{p['dark_fg']}"
red = "{p['bright_red']}"
green = "{p['bright_green']}"
yellow = "{p['bright_yellow']}"
blue = "{p['bright_blue']}"
magenta = "{p['bright_magenta']}"
cyan = "{p['bright_cyan']}"
white = "{p['bright_fg']}"

[colors.line_indicator]
foreground = "None"
background = "{p['lighter_bg']}"

[window]
opacity = 0.97
"""

def gen_kitty_conf(p: dict) -> str:
    return f"""# Ghostwire — Kitty explicit color config
# Merge into ~/.config/kitty/kitty.conf, or `include ~/.config/omarchy/current/theme/kitty.conf`

background            {p['bg']}
foreground            {p['fg']}
cursor                {p['accent']}
cursor_text_color     {p['bg']}
selection_background  {p['selection']}
selection_foreground  {p['fg']}
url_color             {p['accent']}

active_border_color    {p['accent']}
inactive_border_color  {p['dark_fg']}
bell_border_color      {p['red']}

active_tab_background   {p['lighter_bg']}
active_tab_foreground   {p['bright_fg']}
inactive_tab_background {p['dark_bg']}
inactive_tab_foreground {p['dark_fg']}
tab_bar_background      {p['darker_bg']}

# black
color0  {p['color0']}
color8  {p['color8']}
# red
color1  {p['color1']}
color9  {p['color9']}
# green
color2  {p['color2']}
color10 {p['color10']}
# yellow
color3  {p['color3']}
color11 {p['color11']}
# blue
color4  {p['color4']}
color12 {p['color12']}
# magenta
color5  {p['color5']}
color13 {p['color13']}
# cyan
color6  {p['color6']}
color14 {p['color14']}
# white
color7  {p['color7']}
color15 {p['color15']}

background_opacity 0.97
"""

def gen_ghostty_conf(p: dict) -> str:
    return f"""# Ghostwire — Ghostty explicit color config
# Merge into ~/.config/ghostty/config, or `config-file = ~/.config/omarchy/current/theme/ghostty.conf`

background = {p['h_bg']}
foreground = {p['h_fg']}
cursor-color = {p['h_accent']}
cursor-text = {p['h_bg']}
selection-background = {p['h_selection']}
selection-foreground = {p['h_fg']}

palette = 0={p['color0']}
palette = 1={p['color1']}
palette = 2={p['color2']}
palette = 3={p['color3']}
palette = 4={p['color4']}
palette = 5={p['color5']}
palette = 6={p['color6']}
palette = 7={p['color7']}
palette = 8={p['color8']}
palette = 9={p['color9']}
palette = 10={p['color10']}
palette = 11={p['color11']}
palette = 12={p['color12']}
palette = 13={p['color13']}
palette = 14={p['color14']}
palette = 15={p['color15']}

background-opacity = 0.97
unfocused-split-opacity = 0.85
"""

def gen_starship_toml(p: dict) -> str:
    return f'''"$schema" = 'https://starship.rs/config-schema.json'

format = """
$os\\
$username\\
$directory\\
$git_branch\\
$git_status\\
$fill\\
$cmd_duration\\
$line_break\\
$character"""

fill = {{ symbol = " " }}

[os]
disabled = false
style = "bg:{p['magenta']} fg:{p['bright_fg']}"

[os.symbols]
Arch = "󰣇 "
Ubuntu = " "
Fedora = " "
Windows = "󰍲 "

[username]
show_always = true
style_user = "bg:{p['magenta']} fg:{p['bright_fg']}"
style_root = "bg:{p['red']} fg:{p['bright_fg']}"
format = '[ $user ]($style)'

[directory]
style = "bg:{p['selection']} fg:{p['fg']}"
format = "[ $path ]($style)"
truncation_length = 3
truncation_symbol = "…/"

[git_branch]
symbol = ""
style = "bg:{p['bg']} fg:{p['accent']}"
format = '[ $symbol $branch ]($style)'

[git_status]
style = "bg:{p['bg']} fg:{p['yellow']}"
format = '[$all_status$ahead_behind ]($style)'

[cmd_duration]
min_time = 500
style = "fg:{p['dark_fg']}"
format = "[ $duration ]($style)"

[character]
success_symbol = "[❯](bold {p['accent']})"
error_symbol = "[❯](bold {p['red']})"
vimcmd_symbol = "[❮](bold {p['magenta']})"

[nodejs]
symbol = " "
style = "fg:{p['green']}"
format = '[$symbol($version) ]($style)'

[python]
symbol = " "
style = "fg:{p['yellow']}"
format = '[$symbol($version) ]($style)'

[rust]
symbol = "󱘗 "
style = "fg:{p['red']}"
format = '[$symbol($version) ]($style)'

[golang]
symbol = " "
style = "fg:{p['blue']}"
format = '[$symbol($version) ]($style)'

[docker_context]
symbol = " "
style = "fg:{p['blue']}"
format = '[$symbol$context ]($style)'

[package]
symbol = "󰏗 "
style = "fg:{p['magenta']}"
format = '[$symbol$version ]($style)'
'''

def gen_fastfetch_jsonc(p: dict) -> str:
    return f'''{{
  "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
  "logo": {{
    "type": "data",
    "source": "$1        ▄▄▄████████▄▄▄\\n$1     ▄██$1████████████$1██▄\\n$1   ▄██$1████$2▓▓▓▓▓▓$1████$1██▄\\n$1  ██$1████$2▓▓$3██$2▓▓$3██$2▓▓$1████$1██\\n$1 ██$1█████$2▓▓▓▓▓▓▓▓$1█████$1██\\n$1 ██$1█████$2▓▓$1██$1██$2▓▓$1█████$1██\\n$1 ██$1██████$2▓▓▓▓▓▓$1██████$1██\\n$1 ██$1████████████████████$1██\\n$1  ██$1██████████████████$1██\\n$1  ██$1█$1  $1██$1  $1██$1  $1██$1  $1█$1██\\n$1   ██$1█$1 $1██$1 $1██$1 $1██$1 $1█$1██\\n$1    ▀█$1█$1▀$1  $1▀█$1▀$1  $1▀█$1▀\\n$2   G H O S T W I R E",
    "color": {{
      "1": "{p['accent']}",
      "2": "{p['magenta']}",
      "3": "{p['bright_fg']}"
    }},
    "padding": {{ "top": 1, "right": 3 }}
  }},
  "display": {{
    "separator": "  ",
    "color": {{ "keys": "{p['accent']}", "output": "{p['fg']}", "title": "{p['bright_fg']}" }}
  }},
  "modules": [
    {{ "type": "title", "color": {{ "user": "{p['accent']}", "at": "{p['dark_fg']}", "host": "{p['magenta']}" }} }},
    "separator",
    {{ "type": "os", "key": "  OS" }},
    {{ "type": "kernel", "key": "  Kernel" }},
    {{ "type": "packages", "key": "󰏗  Packages" }},
    {{ "type": "shell", "key": "  Shell" }},
    {{ "type": "wm", "key": "  WM" }},
    {{ "type": "terminal", "key": "  Terminal" }},
    {{ "type": "uptime", "key": "  Uptime" }},
    "break",
    {{ "type": "cpu", "key": "  CPU" }},
    {{ "type": "gpu", "key": "󰢮  GPU" }},
    {{ "type": "memory", "key": "  Memory" }},
    {{ "type": "disk", "key": "  Disk" }},
    {{ "type": "localip", "key": "󰩟  LAN" }},
    "break",
    {{
      "type": "colors",
      "symbol": "circle",
      "key": "  Palette"
    }}
  ]
}}
'''

def gen_fzf_fish(p: dict) -> str:
    return f"""# Ghostwire — fzf colors
# Merge into ~/.config/fish/config.fish or source directly.

set -gx FZF_DEFAULT_OPTS "\\
--color=bg+:{p['lighter_bg']},bg:{p['bg']},spinner:{p['accent']},hl:{p['magenta']} \\
--color=fg:{p['fg']},header:{p['magenta']},info:{p['blue']},pointer:{p['accent']} \\
--color=marker:{p['accent']},fg+:{p['bright_fg']},prompt:{p['accent']},hl+:{p['magenta']} \\
--color=selected-bg:{p['selection']} \\
--color=border:{p['border']},label:{p['fg']} \\
--height=40% --layout=reverse --border=rounded"
"""

def gen_colors_fish(p: dict) -> str:
    return f"""# Ghostwire — fish shell syntax-highlight colors
# Merge into ~/.config/fish/config.fish, or:
#   source ~/.config/omarchy/current/theme/colors.fish

set -g fish_color_normal {p['h_fg']}
set -g fish_color_command {p['h_accent']}
set -g fish_color_keyword {p['h_magenta']}
set -g fish_color_quote {p['h_yellow']}
set -g fish_color_redirection {p['h_blue']}
set -g fish_color_end {p['h_dark_fg']}
set -g fish_color_error {p['h_red']}
set -g fish_color_param {p['light_fg'].lstrip('#')}
set -g fish_color_comment {p['h_dark_fg']}
set -g fish_color_selection --background={p['h_selection']}
set -g fish_color_search_match --background={p['h_selection']}
set -g fish_color_operator {p['h_accent']}
set -g fish_color_escape {p['h_magenta']}
set -g fish_color_autosuggestion {p['h_dark_fg']}
set -g fish_color_cancel {p['h_red']}
set -g fish_color_cwd {p['h_accent']}
set -g fish_color_cwd_root {p['h_red']}
set -g fish_color_valid_path --underline

set -g fish_pager_color_prefix {p['h_magenta']} --bold
set -g fish_pager_color_completion {p['h_fg']}
set -g fish_pager_color_description {p['h_dark_fg']}
set -g fish_pager_color_progress {p['h_accent']}
set -g fish_pager_color_selected_background --background={p['h_selection']}
"""

def gen_superfile_toml(p: dict) -> str:
    return f"""# Ghostwire — Superfile (terminal file manager) theme
# Copy to ~/.config/superfile/theme/ghostwire.toml, then set
# `theme = "ghostwire"` in ~/.config/superfile/config.toml
# NOTE: superfile's exact key set can change between versions —
# check `spf --version` / their theme docs if a key here is ignored.

file_panel_border = "{p['border']}"
file_panel_top_directory_icon = "{p['accent']}"
file_panel_top_path = "{p['fg']}"
file_panel_item_selected_fg = "{p['bright_fg']}"
file_panel_item_selected_bg = "{p['selection']}"
file_panel_item = "{p['fg']}"
file_panel_directory_item = "{p['accent']}"

sidebar_title = "{p['magenta']}"
sidebar_item_selected_fg = "{p['bright_fg']}"
sidebar_item_selected_bg = "{p['selection']}"
sidebar_divider = "{p['border']}"
sidebar_bg = "{p['dark_bg']}"

footer_border = "{p['border']}"
footer_path = "{p['accent']}"
footer_selection_total = "{p['fg']}"
footer_cursor_position = "{p['dark_fg']}"

modal_border_activated = "{p['accent']}"
modal_border_deactivated = "{p['dark_fg']}"
modal_title = "{p['bright_fg']}"

full_screen_bg = "{p['bg']}"
help_menu_hotkey = "{p['accent']}"
help_menu_title = "{p['fg']}"

cancel_button = "{p['red']}"
confirm_button = "{p['green']}"
error_display = "{p['red']}"
"""

def gen_zed_json(p: dict) -> str:
    return f"""{{
  "$schema": "https://zed.dev/schema/themes/v0.1.0.json",
  "name": "Ghostwire",
  "author": "Vispobish",
  "themes": [
    {{
      "name": "Ghostwire",
      "appearance": "dark",
      "style": {{
        "border": "{p['border']}ff",
        "border.variant": "{p['border']}ff",
        "border.focused": "{p['accent']}ff",
        "border.selected": "{p['magenta']}ff",
        "background": "{p['bg']}ff",
        "surface.background": "{p['dark_bg']}ff",
        "elevated_surface.background": "{p['lighter_bg']}ff",
        "text": "{p['fg']}ff",
        "text.muted": "{p['dark_fg']}ff",
        "text.accent": "{p['accent']}ff",
        "icon": "{p['fg']}ff",
        "icon.muted": "{p['dark_fg']}ff",
        "element.background": "{p['lighter_bg']}ff",
        "element.hover": "{p['selection']}ff",
        "element.selected": "{p['selection']}ff",
        "tab_bar.background": "{p['darker_bg']}ff",
        "tab.active_background": "{p['bg']}ff",
        "tab.inactive_background": "{p['dark_bg']}ff",
        "editor.background": "{p['bg']}ff",
        "editor.foreground": "{p['fg']}ff",
        "editor.gutter.background": "{p['bg']}ff",
        "editor.line_number": "{p['dark_fg']}ff",
        "editor.active_line_number": "{p['accent']}ff",
        "editor.active_line.background": "{p['lighter_bg']}ff",
        "editor.selection.background": "{p['selection']}66",
        "editor.cursor": "{p['accent']}ff",
        "terminal.background": "{p['bg']}ff",
        "terminal.foreground": "{p['fg']}ff",
        "terminal.ansi.black": "{p['bg']}ff",
        "terminal.ansi.red": "{p['red']}ff",
        "terminal.ansi.green": "{p['green']}ff",
        "terminal.ansi.yellow": "{p['yellow']}ff",
        "terminal.ansi.blue": "{p['blue']}ff",
        "terminal.ansi.magenta": "{p['magenta']}ff",
        "terminal.ansi.cyan": "{p['cyan']}ff",
        "terminal.ansi.white": "{p['fg']}ff",
        "terminal.ansi.bright_black": "{p['dark_fg']}ff",
        "terminal.ansi.bright_red": "{p['bright_red']}ff",
        "terminal.ansi.bright_green": "{p['bright_green']}ff",
        "terminal.ansi.bright_yellow": "{p['bright_yellow']}ff",
        "terminal.ansi.bright_blue": "{p['bright_blue']}ff",
        "terminal.ansi.bright_magenta": "{p['bright_magenta']}ff",
        "terminal.ansi.bright_cyan": "{p['bright_cyan']}ff",
        "terminal.ansi.bright_white": "{p['bright_fg']}ff",
        "syntax": {{
          "keyword": {{ "color": "{p['magenta']}ff", "font_style": null, "font_weight": null }},
          "function": {{ "color": "{p['accent']}ff", "font_style": null, "font_weight": null }},
          "string": {{ "color": "{p['yellow']}ff", "font_style": null, "font_weight": null }},
          "comment": {{ "color": "{p['dark_fg']}ff", "font_style": "italic", "font_weight": null }},
          "type": {{ "color": "{p['blue']}ff", "font_style": null, "font_weight": null }},
          "variable": {{ "color": "{p['fg']}ff", "font_style": null, "font_weight": null }},
          "constant": {{ "color": "{p['bright_red']}ff", "font_style": null, "font_weight": null }},
          "property": {{ "color": "{p['bright_blue']}ff", "font_style": null, "font_weight": null }},
          "number": {{ "color": "{p['bright_yellow']}ff", "font_style": null, "font_weight": null }}
        }}
      }}
    }}
  ]
}}
"""

def gen_vscode_theme(p: dict) -> str:
    return f"""{{
  "name": "Ghostwire",
  "type": "dark",
  "colors": {{
    "focusBorder": "{p['accent']}",
    "foreground": "{p['fg']}",
    "descriptionForeground": "{p['fg']}",
    "errorForeground": "{p['red']}",

    "editor.background": "{p['bg']}",
    "editor.foreground": "{p['fg']}",
    "editorCursor.foreground": "{p['accent']}",
    "editorLineNumber.foreground": "{p['dark_fg']}",
    "editorLineNumber.activeForeground": "{p['accent']}",
    "editor.selectionBackground": "{p['selection']}",
    "editor.selectionHighlightBackground": "{p['selection']}80",
    "editor.inactiveSelectionBackground": "{p['selection']}66",
    "editor.lineHighlightBackground": "{p['lighter_bg']}",
    "editor.wordHighlightBackground": "{p['selection']}80",
    "editor.findMatchBackground": "{p['magenta']}55",
    "editor.findMatchHighlightBackground": "{p['blue']}33",
    "editorIndentGuide.background1": "{p['border']}",
    "editorIndentGuide.activeBackground1": "{p['blue']}55",
    "editorWhitespace.foreground": "{p['border']}",
    "editorRuler.foreground": "{p['border']}",

    "activityBar.background": "{p['darker_bg']}",
    "activityBar.foreground": "{p['accent']}",
    "activityBar.inactiveForeground": "{p['dark_fg']}",
    "activityBar.border": "{p['border']}",
    "activityBarBadge.background": "{p['magenta']}",
    "activityBarBadge.foreground": "{p['darker_bg']}",

    "sideBar.background": "{p['bg']}",
    "sideBar.border": "{p['border']}",
    "sideBar.foreground": "{p['fg']}",
    "sideBarTitle.foreground": "{p['bright_fg']}",
    "sideBarSectionHeader.background": "{p['bg']}",
    "sideBarSectionHeader.border": "{p['border']}",
    "list.activeSelectionBackground": "{p['selection']}",
    "list.activeSelectionForeground": "{p['bright_fg']}",
    "list.inactiveSelectionBackground": "{p['selection']}66",
    "list.hoverBackground": "{p['lighter_bg']}",
    "list.highlightForeground": "{p['accent']}",
    "tree.indentGuidesStroke": "{p['border']}",

    "statusBar.background": "{p['bg']}",
    "statusBar.foreground": "{p['fg']}",
    "statusBar.border": "{p['border']}",
    "statusBar.debuggingBackground": "{p['red']}",
    "statusBar.debuggingForeground": "{p['darker_bg']}",
    "statusBar.noFolderBackground": "{p['darker_bg']}",
    "statusBarItem.hoverBackground": "{p['lighter_bg']}",
    "statusBarItem.remoteBackground": "{p['accent']}",
    "statusBarItem.remoteForeground": "{p['darker_bg']}",

    "titleBar.activeBackground": "{p['dark_bg']}",
    "titleBar.activeForeground": "{p['fg']}",
    "titleBar.inactiveBackground": "{p['darker_bg']}",
    "titleBar.inactiveForeground": "{p['dark_fg']}",
    "titleBar.border": "{p['border']}",

    "tab.activeBackground": "{p['bg']}",
    "tab.activeForeground": "{p['bright_fg']}",
    "tab.activeBorder": "{p['accent']}",
    "tab.inactiveBackground": "{p['dark_bg']}",
    "tab.inactiveForeground": "{p['dark_fg']}",
    "tab.border": "{p['border']}",
    "editorGroupHeader.tabsBackground": "{p['dark_bg']}",
    "editorGroupHeader.tabsBorder": "{p['border']}",

    "terminal.background": "{p['bg']}",
    "terminal.foreground": "{p['fg']}",
    "terminal.ansiBlack": "{p['color0']}",
    "terminal.ansiRed": "{p['color1']}",
    "terminal.ansiGreen": "{p['color2']}",
    "terminal.ansiYellow": "{p['color3']}",
    "terminal.ansiBlue": "{p['color4']}",
    "terminal.ansiMagenta": "{p['color5']}",
    "terminal.ansiCyan": "{p['color6']}",
    "terminal.ansiWhite": "{p['color7']}",
    "terminal.ansiBrightBlack": "{p['color8']}",
    "terminal.ansiBrightRed": "{p['color9']}",
    "terminal.ansiBrightGreen": "{p['color10']}",
    "terminal.ansiBrightYellow": "{p['color11']}",
    "terminal.ansiBrightBlue": "{p['color12']}",
    "terminal.ansiBrightMagenta": "{p['color13']}",
    "terminal.ansiBrightCyan": "{p['color14']}",
    "terminal.ansiBrightWhite": "{p['color15']}",

    "input.background": "{p['dark_bg']}",
    "input.foreground": "{p['bright_fg']}",
    "input.border": "{p['border']}",
    "input.placeholderForeground": "{p['dark_fg']}",
    "inputOption.activeBorder": "{p['accent']}",

    "dropdown.background": "{p['dark_bg']}",
    "dropdown.foreground": "{p['fg']}",
    "dropdown.border": "{p['border']}",

    "badge.background": "{p['magenta']}",
    "badge.foreground": "{p['darker_bg']}",

    "scrollbarSlider.background": "{p['selection']}80",
    "scrollbarSlider.hoverBackground": "{p['border']}",
    "scrollbarSlider.activeBackground": "{p['blue']}55",

    "progressBar.background": "{p['accent']}",

    "notificationCenterHeader.background": "{p['dark_bg']}",
    "notifications.background": "{p['dark_bg']}",
    "notifications.foreground": "{p['fg']}",
    "notifications.border": "{p['border']}",
    "notificationLink.foreground": "{p['accent']}",

    "peekView.border": "{p['accent']}",
    "peekViewEditor.background": "{p['dark_bg']}",
    "peekViewResult.background": "{p['darker_bg']}",
    "peekViewResult.selectionBackground": "{p['selection']}",
    "peekViewResult.selectionForeground": "{p['bright_fg']}",

    "gitDecoration.addedResourceForeground": "{p['green']}",
    "gitDecoration.modifiedResourceForeground": "{p['yellow']}",
    "gitDecoration.deletedResourceForeground": "{p['red']}",
    "gitDecoration.untrackedResourceForeground": "{p['accent']}",
    "gitDecoration.ignoredResourceForeground": "{p['dark_fg']}",

    "button.background": "{p['accent']}",
    "button.foreground": "{p['darker_bg']}",
    "button.hoverBackground": "{p['bright_cyan']}",
    "button.secondaryBackground": "{p['lighter_bg']}",
    "button.secondaryForeground": "{p['fg']}",
    "button.secondaryHoverBackground": "{p['selection']}",
    "extensionButton.prominentBackground": "{p['accent']}",
    "extensionButton.prominentForeground": "{p['darker_bg']}",
    "extensionButton.prominentHoverBackground": "{p['bright_cyan']}"
  }},
  "tokenColors": [
    {{
      "scope": ["comment", "punctuation.definition.comment"],
      "settings": {{ "foreground": "{p['dark_fg']}", "fontStyle": "italic" }}
    }},
    {{
      "scope": ["string", "punctuation.definition.string"],
      "settings": {{ "foreground": "{p['green']}" }}
    }},
    {{
      "scope": ["constant.numeric", "constant.language"],
      "settings": {{ "foreground": "{p['bright_yellow']}" }}
    }},
    {{
      "scope": ["variable", "variable.other"],
      "settings": {{ "foreground": "{p['light_fg']}" }}
    }},
    {{
      "scope": ["variable.parameter"],
      "settings": {{ "foreground": "{p['light_fg']}", "fontStyle": "italic" }}
    }},
    {{
      "scope": ["keyword", "storage.type", "storage.modifier"],
      "settings": {{ "foreground": "{p['bright_magenta']}", "fontStyle": "italic" }}
    }},
    {{
      "scope": ["keyword.operator"],
      "settings": {{ "foreground": "{p['magenta']}", "fontStyle": "bold" }}
    }},
    {{
      "scope": ["entity.name.function", "support.function"],
      "settings": {{ "foreground": "{p['blue']}" }}
    }},
    {{
      "scope": ["entity.name.type", "entity.name.class", "support.class", "support.type"],
      "settings": {{ "foreground": "{p['accent']}", "fontStyle": "bold" }}
    }},
    {{
      "scope": ["entity.name.tag"],
      "settings": {{ "foreground": "{p['blue']}" }}
    }},
    {{
      "scope": ["entity.other.attribute-name"],
      "settings": {{ "foreground": "{p['blue']}", "fontStyle": "italic" }}
    }},
    {{
      "scope": ["constant.other.symbol", "constant.other.key"],
      "settings": {{ "foreground": "{p['magenta']}" }}
    }},
    {{
      "scope": ["constant.character.escape"],
      "settings": {{ "foreground": "{p['bright_yellow']}" }}
    }},
    {{
      "scope": ["support.type.property-name", "meta.object-literal.key"],
      "settings": {{ "foreground": "{p['bright_blue']}" }}
    }},
    {{
      "scope": ["punctuation", "meta.brace", "punctuation.definition.parameters"],
      "settings": {{ "foreground": "{p['light_fg']}" }}
    }},
    {{
      "scope": ["keyword.control.import", "keyword.control.from", "meta.import"],
      "settings": {{ "foreground": "{p['bright_cyan']}" }}
    }},
    {{
      "scope": ["invalid", "invalid.illegal"],
      "settings": {{ "foreground": "{p['red']}" }}
    }},
    {{
      "scope": ["markup.heading"],
      "settings": {{ "fontStyle": "bold", "foreground": "{p['bright_fg']}" }}
    }},
    {{
      "scope": ["markup.bold"],
      "settings": {{ "fontStyle": "bold" }}
    }},
    {{
      "scope": ["markup.italic"],
      "settings": {{ "fontStyle": "italic" }}
    }},
    {{
      "scope": ["markup.link"],
      "settings": {{ "foreground": "{p['accent']}", "fontStyle": "bold" }}
    }},
    {{
      "scope": ["markup.raw.inline", "markup.raw.block"],
      "settings": {{ "foreground": "{p['yellow']}" }}
    }},
    {{
      "scope": ["markup.inserted"],
      "settings": {{ "foreground": "{p['accent']}" }}
    }},
    {{
      "scope": ["markup.changed"],
      "settings": {{ "foreground": "{p['yellow']}" }}
    }},
    {{
      "scope": ["markup.deleted"],
      "settings": {{ "foreground": "{p['red']}" }}
    }}
  ]
}}
"""

def gen_cliamp_theme(p: dict) -> str:
    return f"""# Ghostwire — cliamp theme
# cliamp loads themes from ~/.config/cliamp/themes/*.toml (filename minus
# .toml = theme name shown in its theme picker). Install:
#   mkdir -p ~/.config/cliamp/themes
#   cp cliamp.theme ~/.config/cliamp/themes/ghostwire.toml
# Then open cliamp, press `t` (Choose theme), and select "ghostwire".
#
# Key names must match exactly (cliamp's parser is a flat key=value scanner,
# not a full TOML parser, and silently drops any theme that fails
# validation): bg, accent, bright_fg, fg, green, yellow, red. `bg` is
# optional; the other five are required and must be #RRGGBB.

name = "Ghostwire"
bg = "{p['bg']}"
accent = "{p['accent']}"
bright_fg = "{p['bright_fg']}"
fg = "{p['fg']}"
green = "{p['green']}"
yellow = "{p['yellow']}"
red = "{p['red']}"
"""

def gen_firefox_userchrome_css(p: dict) -> str:
    return f"""/* Ghostwire — Firefox userChrome.css
 * Requires toolkit.legacyUserProfileCustomizations.stylesheets = true in
 * about:config, then place this + userContent.css in
 * <profile>/chrome/ (create the folder if it doesn't exist) and restart.
 */

:root {{
  --toolbar-bgcolor: {p['bg']} !important;
  --toolbar-color: {p['fg']} !important;
  --lwt-accent-color: {p['bg']} !important;
  --lwt-text-color: {p['fg']} !important;
  --tab-selected-bgcolor: {p['selection']} !important;
  --tabpanel-background-color: {p['bg']} !important;
  --urlbar-box-bgcolor: {p['lighter_bg']} !important;
  --urlbar-box-focus-bgcolor: {p['lighter_bg']} !important;
  --toolbarbutton-icon-fill: {p['fg']} !important;
  --toolbarbutton-hover-background: {p['selection']} !important;
}}

#navigator-toolbox,
#nav-bar,
#PersonalToolbar,
#TabsToolbar {{
  background-color: {p['bg']} !important;
  border-color: {p['border']} !important;
}}

.tabbrowser-tab[selected="true"] .tab-background {{
  background-color: {p['selection']} !important;
  border-radius: 8px !important;
}}

.tabbrowser-tab .tab-background {{
  border-radius: 8px !important;
}}

#tabbrowser-tabs .tab-content .tab-label {{
  color: {p['fg']} !important;
}}

#urlbar,
#searchbar {{
  background-color: {p['lighter_bg']} !important;
  color: {p['bright_fg']} !important;
  border: 1px solid {p['border']} !important;
  border-radius: 8px !important;
}}

#urlbar[focused="true"] {{
  border-color: {p['accent']} !important;
}}

.urlbar-input {{
  color: {p['bright_fg']} !important;
}}

/* cyan accent on the active tab's top border */
.tabbrowser-tab[selected="true"] .tab-line {{
  background-color: {p['accent']} !important;
}}

toolbarbutton:hover {{
  background-color: {p['selection']} !important;
  border-radius: 6px !important;
}}
"""

def gen_firefox_usercontent_css(p: dict) -> str:
    return f"""/* Ghostwire — Firefox userContent.css
 * Styles Firefox's own pages (about:newtab, about:config, reader mode, the
 * built-in PDF viewer) — not arbitrary websites. Same install steps as
 * userChrome.css: needs toolkit.legacyUserProfileCustomizations.stylesheets
 * enabled, lives alongside it in <profile>/chrome/.
 */

@-moz-document url(about:newtab), url(about:home), url(about:blank) {{
  :root {{
    background-color: {p['bg']} !important;
  }}
}}

@-moz-document url-prefix(about:config) {{
  body {{ background-color: {p['bg']} !important; color: {p['fg']} !important; }}
}}

@-moz-document url-prefix(about:reader) {{
  body.dark {{
    background-color: {p['bg']} !important;
  }}
  .container {{
    background-color: {p['bg']} !important;
    color: {p['fg']} !important;
  }}
  a {{ color: {p['accent']} !important; }}
}}

@-moz-document url-prefix(resource://pdf.js) {{
  :root {{
    --toolbar-bg-color: {p['bg']} !important;
    --body-bg-color: {p['darker_bg']} !important;
    --main-color: {p['fg']} !important;
  }}
}}
"""

def gen_zen_css(p: dict) -> str:
    return f"""/* Ghostwire — Zen Browser (Firefox fork) chrome
   Zen uses the same userChrome.css mechanism as Firefox. This is a thin
   pointer file — the real rules live in firefox/userChrome.css and
   firefox/userContent.css, which apply as-is to Zen's profile chrome
   folder (enable toolkit.legacyUserProfileCustomizations.stylesheets in
   about:config, same as Firefox). Copy both files to:
     <zen-profile>/chrome/userChrome.css
     <zen-profile>/chrome/userContent.css
   Zen-specific accent: set Settings > Zen > Theme > Accent Color to
   {p['accent']} to match the rest of the identity in Zen's native UI (tabs
   sidebar, workspaces, compact mode) that userChrome.css doesn't reach. */
"""

def gen_vencord_theme_css(p: dict) -> str:
    return f"""/**
 * @name Ghostwire
 * @author Vispobish
 * @version 1.0.0
 * @description Ghostwire theme for Vencord/Discord — dark teal/purple instrument panel
 * @website https://github.com/vispobish01-netizen/omarchy-ghostwire-theme
 */

:root {{
  /* Background surfaces */
  --background-primary: {p['bg']} !important;
  --background-secondary: {p['dark_bg']} !important;
  --background-secondary-alt: {p['darker_bg']} !important;
  --background-tertiary: {p['darker_bg']} !important;
  --background-floating: {p['dark_bg']} !important;
  --background-accent: {p['lighter_bg']} !important;
  --channeltextarea-background: {p['lighter_bg']} !important;

  /* Borders & dividers */
  --border-faint: {p['border']} !important;

  /* Typography */
  --text-normal: {p['fg']} !important;
  --text-muted: {p['dark_fg']} !important;
  --text-link: {p['accent']} !important;
  --header-primary: {p['bright_fg']} !important;
  --header-secondary: {p['fg']} !important;

  --interactive-normal: {p['fg']} !important;
  --interactive-hover: {p['bright_fg']} !important;
  --interactive-active: {p['bright_fg']} !important;
  --interactive-muted: {p['dark_fg']} !important;

  --brand-experiment: {p['accent']} !important;
  --brand-experiment-560: {p['blue']} !important;

  --background-modifier-hover: rgba(80, 220, 200, 0.08) !important;
  --background-modifier-selected: {p['selection']} !important;
  --background-modifier-active: rgba(80, 220, 200, 0.16) !important;

  /* Scrollbars */
  --scrollbar-auto-thumb: {p['border']} !important;
  --scrollbar-auto-track: transparent !important;
  --scrollbar-thin-thumb: {p['border']} !important;

  /* Accents */
  --status-positive: {p['green']} !important;
  --status-warning: {p['yellow']} !important;
  --status-danger: {p['red']} !important;
  --info-positive-background: rgba(80, 200, 120, 0.1) !important;
  --info-warning-background: rgba(220, 180, 60, 0.1) !important;
  --info-danger-background: rgba(220, 80, 80, 0.1) !important;

  /* Buttons */
  --button-primary-background: {p['accent']} !important;
  --button-primary-text: {p['darker_bg']} !important;
  --button-secondary-background: {p['lighter_bg']} !important;
  --button-danger-background: {p['red']} !important;
}}

/* Unread badges */
.unread__3b95d {{
  background-color: {p['accent']} !important;
}}

.badge__92713 {{
  background-color: {p['magenta']} !important;
  color: {p['bright_fg']} !important;
}}
"""

def gen_telegram_tdesktop_theme(p: dict) -> str:
    # Outgoing bubble: deep teal-tinted dark (#0f1c20)
    # Incoming bubble: slightly lighter than bg (#151b26)
    return f"""// Ghostwire Theme for Telegram Desktop
// Single-source derived from colors.toml
// Brand: Dark "instrument panel" feel, cyan -> purple identity

// Base Palette Definitions
pBg: {p['bg']};
pDarkBg: {p['dark_bg']};
pDarkerBg: {p['darker_bg']};
pLighterBg: {p['lighter_bg']};
pFg: {p['fg']};
pBrightFg: {p['bright_fg']};
pDim: {p['dark_fg']};
pBorder: {p['border']};
pSelection: {p['selection']};

pCyan: {p['accent']};
pPurple: {p['magenta']};
pBlue: {p['blue']};
pGreen: {p['green']};
pYellow: {p['yellow']};
pRed: {p['red']};

// Window & Shell Chrome
windowBg: pBg;
windowFg: pFg;
windowBgOver: pLighterBg;
windowBgRipple: pSelection;
windowFgOver: windowFg;
windowSubTextFg: pDim;
windowSubTextFgOver: pPurple;
windowBoldFg: pBrightFg;
windowBoldFgOver: pCyan;
windowBgActive: pCyan;
windowFgActive: pDarkerBg;
windowActiveTextFg: pCyan;
windowShadowFg: #00000080;
windowShadowFgFallback: pDarkerBg;
shadowFg: #00000028;

slideFadeOutBg: #00000040;
slideFadeOutShadowFg: windowShadowFg;
imageBg: #000000;
imageBgTransparent: pBg;

// Interactive Buttons & Controls
activeButtonBg: pCyan;
activeButtonBgOver: {p['bright_cyan']};
activeButtonBgRipple: pSelection;
activeButtonFg: pDarkerBg;
activeButtonFgOver: pDarkerBg;
activeButtonSecondaryFg: pDarkerBg;
activeButtonSecondaryFgOver: pDarkerBg;
activeLineFg: pCyan;
activeLineFgError: pRed;

lightButtonBg: pBg;
lightButtonBgOver: pLighterBg;
lightButtonBgRipple: pSelection;
lightButtonFg: pCyan;
lightButtonFgOver: pCyan;

attentionButtonFg: pRed;
attentionButtonFgOver: pBrightFg;
attentionButtonBgOver: #dc505040;
attentionButtonBgRipple: pSelection;

outlineButtonBg: pBg;
outlineButtonBgOver: pLighterBg;
outlineButtonOutlineFg: pCyan;
outlineButtonBgRipple: pSelection;

// Popup Menus
menuBg: pDarkBg;
menuBgOver: pLighterBg;
menuBgRipple: pSelection;
menuIconFg: pDim;
menuIconFgOver: pCyan;
menuSubmenuArrowFg: pDim;
menuFgDisabled: pDim;
menuSeparatorFg: pBorder;

// Scrollbars
scrollBarBg: {p['dark_fg']}60;
scrollBarBgOver: {p['accent']}a0;
scrollBg: #00000000;
scrollBgOver: #00000010;

// Inputs & Modals
smallCloseIconFg: pDim;
smallCloseIconFgOver: pRed;
radialFg: pCyan;
radialBg: #00000050;
placeholderFg: pDim;
placeholderFgActive: pDim;
inputBorderFg: pBorder;
filterInputBorderFg: pCyan;
filterInputActiveBg: pDarkBg;
filterInputInactiveBg: pDarkerBg;
checkboxFg: pDim;
sliderBgInactive: pLighterBg;
sliderBgActive: pCyan;

tooltipBg: pDarkBg;
tooltipFg: pFg;
tooltipBorderFg: pBorder;

// Dialogs & Chats List
dialogsBg: pBg;
dialogsBgOver: pDarkBg;
dialogsBgActive: pSelection;
dialogsNameFg: pFg;
dialogsNameFgOver: pBrightFg;
dialogsNameFgActive: pBrightFg;
dialogsChatIconFg: pCyan;
dialogsDateFg: pDim;
dialogsDateFgOver: pDim;
dialogsDateFgActive: pCyan;
dialogsTextFg: pDim;
dialogsTextFgOver: pFg;
dialogsTextFgActive: pFg;
dialogsTextFgService: pCyan;
dialogsDraftFg: pYellow;
dialogsVerifiedIconBg: pCyan;
dialogsVerifiedIconFg: pDarkerBg;
dialogsSendingIconFg: pDim;
dialogsSentIconFg: pCyan;
dialogsUnreadBg: pCyan;
dialogsUnreadBgMuted: pDim;
dialogsUnreadFg: pDarkerBg;
dialogsUnreadFgMuted: pFg;

// Message Bubbles & Chat History
// Outgoing bubble: deep teal-tinted dark (#0f1c20), incoming: slightly lighter than bg (#151b26)
msgInBg: #151b26;
msgInBgSelected: pSelection;
msgOutBg: #0f1c20;
msgOutBgSelected: #182c32;

historyTextInFg: pFg;
historyTextInFgSelected: pBrightFg;
historyTextOutFg: pFg;
historyTextOutFgSelected: pBrightFg;

historyLinkInFg: pBlue;
historyLinkInFgSelected: pCyan;
historyLinkOutFg: pCyan;
historyLinkOutFgSelected: pBrightFg;

historyFileNameInFg: pCyan;
historyFileNameOutFg: pCyan;
msgInDateFg: pDim;
msgInDateFgSelected: pDim;
msgOutDateFg: {p['accent']}88;
msgOutDateFgSelected: pCyan;

msgInShadow: #00000000;
msgOutShadow: #00000000;
msgServiceBg: {p['bg']}b0;
msgServiceFg: pBrightFg;

// Peer Userpic and Highlight Palette
historyPeer1NameFg: pRed;
historyPeer2NameFg: pGreen;
historyPeer3NameFg: pYellow;
historyPeer4NameFg: pBlue;
historyPeer5NameFg: pPurple;
historyPeer6NameFg: {p['bright_red']};
historyPeer7NameFg: pCyan;
historyPeer8NameFg: {p['bright_yellow']};

historyPeerUserpicBg1: pRed;
historyPeerUserpicBg2: pGreen;
historyPeerUserpicBg3: pYellow;
historyPeerUserpicBg4: pBlue;
historyPeerUserpicBg5: pPurple;
historyPeerUserpicBg6: {p['bright_red']};
historyPeerUserpicBg7: pCyan;
historyPeerUserpicBg8: {p['bright_yellow']};
"""

def gen_obsidian_css(p: dict) -> str:
    return f"""/* Ghostwire Theme for Obsidian
 * Derived from colors.toml
 */

.theme-dark, .theme-light {{
  --background-primary: {p['bg']};
  --background-primary-alt: {p['dark_bg']};
  --background-secondary: {p['dark_bg']};
  --background-secondary-alt: {p['darker_bg']};
  --text-normal: {p['fg']};

  --text-selection: {p['selection']};
  --background-modifier-border: {p['border']};

  --text-title-h1: {p['accent']};
  --text-title-h2: {p['magenta']};
  --text-title-h3: {p['blue']};
  --text-title-h4: {p['green']};
  --text-title-h5: {p['yellow']};
  --text-title-h6: {p['red']};

  --text-link: {p['blue']};
  --text-accent: {p['accent']};
  --text-accent-hover: {p['bright_cyan']};
  --interactive-accent: {p['accent']};
  --interactive-accent-hover: {p['bright_cyan']};

  --text-muted: {p['dark_fg']};
  --code-normal: {p['accent']};

  --text-error: {p['red']};
  --text-success: {p['green']};

  --tag-color: {p['accent']};
  --tag-background: {p['lighter_bg']};

  --graph-line: {p['border']};
  --graph-node: {p['accent']};
  --graph-node-focused: {p['magenta']};
  --graph-node-tag: {p['cyan']};
  --graph-node-attachment: {p['green']};
}}

.cm-header-1, .markdown-rendered h1 {{ color: var(--text-title-h1); font-weight: bold; }}
.cm-header-2, .markdown-rendered h2 {{ color: var(--text-title-h2); font-weight: bold; }}
.cm-header-3, .markdown-rendered h3 {{ color: var(--text-title-h3); font-weight: bold; }}
.cm-header-4, .markdown-rendered h4 {{ color: var(--text-title-h4); font-weight: bold; }}
"""

def gen_lazygit_yml(p: dict) -> str:
    return f"""# Ghostwire theme for lazygit
# Merge into ~/.config/lazygit/config.yml under `gui:`
gui:
  theme:
    activeBorderColor:
      - '{p['accent']}'
      - bold
    inactiveBorderColor:
      - '{p['border']}'
    optionsTextColor:
      - '{p['blue']}'
    selectedLineBgColor:
      - '{p['selection']}'
    cherryPickedCommitBgColor:
      - '{p['magenta']}'
    cherryPickedCommitFgColor:
      - '{p['bright_fg']}'
    unstagedChangesColor:
      - '{p['red']}'
    defaultFgColor:
      - '{p['fg']}'
    searchingActiveBorderColor:
      - '{p['yellow']}'
"""

def gen_yazi_toml(p: dict) -> str:
    return f"""# Ghostwire theme for yazi
# Copy to ~/.config/yazi/theme.toml

[manager]
cwd = {{ fg = "{p['accent']}" }}
hovered = {{ fg = "{p['bright_fg']}", bg = "{p['selection']}" }}
preview_hovered = {{ underline = true }}
find_keyword = {{ fg = "{p['yellow']}", bold = true }}
find_position = {{ fg = "{p['magenta']}", italic = true }}
border_symbol = "│"
border_style = {{ fg = "{p['border']}" }}

[status]
separator_open = ""
separator_close = ""
separator_style = {{ fg = "{p['border']}", bg = "{p['border']}" }}
mode_normal = {{ fg = "{p['darker_bg']}", bg = "{p['accent']}", bold = true }}
mode_select = {{ fg = "{p['darker_bg']}", bg = "{p['magenta']}", bold = true }}
mode_unset = {{ fg = "{p['darker_bg']}", bg = "{p['red']}", bold = true }}

[select]
border = {{ fg = "{p['border']}" }}
active = {{ fg = "{p['accent']}", bold = true }}
inactive = {{ fg = "{p['fg']}" }}

[input]
border = {{ fg = "{p['accent']}" }}
title = {{ fg = "{p['bright_fg']}" }}
value = {{ fg = "{p['fg']}" }}
"""

def gen_tmux_conf(p: dict) -> str:
    return f"""# Ghostwire theme for tmux
# Merge into ~/.tmux.conf

set -g status-style "bg={p['bg']},fg={p['fg']}"
set -g status-left "#[bg={p['magenta']},fg={p['bright_fg']},bold] #S #[bg={p['bg']},fg={p['magenta']}] "
set -g status-right "#[fg={p['dark_fg']}]%Y-%m-%d #[fg={p['accent']},bold]%H:%M #[bg={p['accent']},fg={p['darker_bg']},bold] #h "
set -g window-status-current-style "bg={p['selection']},fg={p['accent']},bold"
set -g window-status-style "bg={p['bg']},fg={p['dark_fg']}"
set -g pane-border-style "fg={p['border']}"
set -g pane-active-border-style "fg={p['accent']}"
set -g message-style "bg={p['dark_bg']},fg={p['accent']}"
"""

def gen_wezterm_lua(p: dict) -> str:
    return f"""-- Ghostwire theme for WezTerm
-- Return as color scheme table or put in colors/ghostwire.toml

return {{
  colors = {{
    foreground = "{p['fg']}",
    background = "{p['bg']}",
    cursor_bg = "{p['accent']}",
    cursor_fg = "{p['bg']}",
    cursor_border = "{p['accent']}",
    selection_fg = "{p['fg']}",
    selection_bg = "{p['selection']}",

    ansi = {{
      "{p['color0']}",
      "{p['color1']}",
      "{p['color2']}",
      "{p['color3']}",
      "{p['color4']}",
      "{p['color5']}",
      "{p['color6']}",
      "{p['color7']}",
    }},
    brights = {{
      "{p['color8']}",
      "{p['color9']}",
      "{p['color10']}",
      "{p['color11']}",
      "{p['color12']}",
      "{p['color13']}",
      "{p['color14']}",
      "{p['color15']}",
    }},
  }}
}}
"""

def gen_spicetify_ini(p: dict) -> str:
    return f"""[ghostwire]
accent             = {p['h_accent']}
accent-active      = {p['h_accent']}
accent-inactive    = {p['h_dark_fg']}
banner             = {p['h_accent']}
border-active      = {p['h_accent']}
border-inactive    = {p['h_border']}
header             = {p['h_fg']}
highlight          = {p['h_selection']}
main               = {p['h_bg']}
notification       = {p['h_accent']}
notification-error = {p['h_red']}
subtext            = {p['h_dark_fg']}
text               = {p['h_fg']}
"""

def gen_chromium_theme(p: dict) -> str:
    h = p['bg'].lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}\n"

def get_file_generators():
    return [
        ("chromium.theme", gen_chromium_theme),
        ("gtk.css", gen_gtk_css),
        ("waybar.css", gen_waybar_css),
        ("walker.css", gen_walker_css),
        ("mako.ini", gen_mako_ini),
        ("swayosd.css", gen_swayosd_css),
        ("cava_theme", gen_cava_theme),
        ("starship.toml", gen_starship_toml),
        ("fastfetch.jsonc", gen_fastfetch_jsonc),
        ("fzf.fish", gen_fzf_fish),
        ("colors.fish", gen_colors_fish),
        ("superfile.toml", gen_superfile_toml),
        ("zed.json", gen_zed_json),
        ("vscode-theme/themes/ghostwire-color-theme.json", gen_vscode_theme),
        ("cliamp.theme", gen_cliamp_theme),
        ("firefox/userChrome.css", gen_firefox_userchrome_css),
        ("firefox/userContent.css", gen_firefox_usercontent_css),
        ("zen.css", gen_zen_css),
        ("vencord.theme.css", gen_vencord_theme_css),
        ("telegram/colors.tdesktop-theme", gen_telegram_tdesktop_theme),
        ("obsidian.css", gen_obsidian_css),
        ("lazygit.yml", gen_lazygit_yml),
        ("yazi.toml", gen_yazi_toml),
        ("tmux.conf", gen_tmux_conf),
        ("wezterm.lua.example", gen_wezterm_lua),
        ("spicetify/color.ini", gen_spicetify_ini),
    ]

def main():
    parser = argparse.ArgumentParser(description="Ghostwire Theme Palette Generator")
    parser.add_argument("--check", action="store_true", help="Fail if any generated file is out of sync with colors.toml")
    args = parser.parse_args()

    colors_toml = ROOT / "colors.toml"
    if not colors_toml.exists():
        print(f"Error: {colors_toml} not found!", file=sys.stderr)
        sys.exit(2)

    palette = load_palette(colors_toml)
    generators = get_file_generators()

    out_of_sync = []
    updated = []

    for rel_path, gen_func in generators:
        target = ROOT / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        content = gen_func(palette)

        if args.check:
            if not target.exists():
                out_of_sync.append((rel_path, "missing"))
            else:
                existing = target.read_text(encoding="utf-8")
                if existing != content:
                    out_of_sync.append((rel_path, "content mismatch"))
        else:
            target.write_text(content, encoding="utf-8")
            updated.append(rel_path)

    if args.check:
        if out_of_sync:
            print("❌ The following generated files are out of sync with colors.toml:", file=sys.stderr)
            for path, reason in out_of_sync:
                print(f"  - {path} ({reason})", file=sys.stderr)
            print("\nRun 'python3 scripts/generate.py' to synchronize.", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"✅ All {len(generators)} generated files are in sync with colors.toml.")
            sys.exit(0)
    else:
        print(f"✨ Successfully generated {len(updated)} theme files from colors.toml.")

if __name__ == "__main__":
    main()
