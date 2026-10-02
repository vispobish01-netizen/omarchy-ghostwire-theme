-- Ghostwire — Hyprland theme overrides
-- Identity: signature teal/cyan + purple neon on near-black glass

local active_border_color = { colors = { "rgba(50dcc8ee)", "rgba(9664dcee)" }, angle = 45 }
local inactive_border_color = "rgba(3a425099)"

hl.config({
  general = {
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
    gaps_in = 4,
    gaps_out = 8,
    border_size = 2,
  },

  decoration = {
    rounding = 8,
    active_opacity = 1.0,
    inactive_opacity = 0.96,

    shadow = {
      enabled = true,
      range = 18,
      render_power = 3,
      color = "rgba(06070cbb)",
    },

    blur = {
      enabled = false,
    },
  },

  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },
  },
})

-- Smooth, responsive easing
hl.curve("ghostwireEase", { type = "bezier", points = { { 0.16, 1 }, { 0.3, 1 } } })

hl.animation({ leaf = "windows", enabled = true, speed = 4, bezier = "ghostwireEase", style = "slide" })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 4, bezier = "ghostwireEase", style = "slide" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 2.5, bezier = "ghostwireEase", style = "slide" })
hl.animation({ leaf = "border", enabled = true, speed = 5, bezier = "ghostwireEase" })
hl.animation({ leaf = "fade", enabled = true, speed = 3, bezier = "ghostwireEase" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 4, bezier = "ghostwireEase", style = "slide" })
