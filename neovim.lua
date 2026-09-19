-- Ghostwire — Neovim colorscheme
-- Matches ghostwire/colors.toml (teal/cyan + purple on near-black).
--
-- This is a self-contained colorscheme (no plugin dependency), so it works
-- whether or not you use LazyVim. Two ways to use it:
--
-- 1) Standalone (any nvim config):
--      mkdir -p ~/.config/nvim/colors
--      cp neovim.lua ~/.config/nvim/colors/ghostwire.lua
--      :colorscheme ghostwire
--
-- 2) As the live Omarchy theme (auto-switches with `omarchy-theme-set`):
--      symlink ~/.config/omarchy/current/theme/neovim.lua into your nvim
--      colors/ dir, e.g. via a small lazy.nvim plugin, or just re-run step 1
--      after each `omarchy-theme-set ghostwire` (Omarchy keeps this file in
--      sync with colors.toml since it's a hand-written theme, not generated).

vim.cmd("hi clear")
if vim.fn.exists("syntax_on") == 1 then
	vim.cmd("syntax reset")
end
vim.o.termguicolors = true
vim.o.background = "dark"
vim.g.colors_name = "ghostwire"

local c = {
	bg = "#08090d",
	bg_dark = "#090c11",
	bg_darker = "#06070c",
	bg_light = "#151b26",
	fg = "#c8d2e6",
	fg_dim = "#3a4250",
	fg_light = "#d8e1f2",
	fg_bright = "#e8f7f4",
	sel_bg = "#1c2740",
	border = "#1a2233",
	cyan = "#50dcc8",
	blue = "#3fc4de",
	purple = "#9664dc",
	green = "#50c878",
	yellow = "#dcb43c",
	orange = "#d9792f",
	red = "#dc5050",
	bright_red = "#ec6a88",
	bright_yellow = "#fab795",
	bright_green = "#7ee8a8",
	bright_cyan = "#6be4e6",
	bright_blue = "#6fb0e8",
	bright_magenta = "#b98ae8",
	none = "NONE",
}

local hl = vim.api.nvim_set_hl

local groups = {
	-- Editor UI
	Normal = { fg = c.fg, bg = c.bg },
	NormalFloat = { fg = c.fg, bg = c.bg_dark },
	NormalNC = { fg = c.fg, bg = c.bg },
	FloatBorder = { fg = c.cyan, bg = c.bg_dark },
	SignColumn = { fg = c.fg_dim, bg = c.bg },
	ColorColumn = { bg = c.bg_light },
	Cursor = { fg = c.bg, bg = c.fg_bright },
	CursorLine = { bg = c.bg_light },
	CursorLineNr = { fg = c.cyan, bold = true },
	LineNr = { fg = c.fg_dim },
	Visual = { bg = c.sel_bg },
	VisualNOS = { bg = c.sel_bg },
	Search = { fg = c.bg, bg = c.yellow },
	IncSearch = { fg = c.bg, bg = c.cyan },
	CurSearch = { fg = c.bg, bg = c.cyan },
	Substitute = { fg = c.bg, bg = c.orange },
	MatchParen = { fg = c.cyan, bold = true, underline = true },

	StatusLine = { fg = c.fg_light, bg = c.bg_dark },
	StatusLineNC = { fg = c.fg_dim, bg = c.bg_dark },
	WinSeparator = { fg = c.border },
	VertSplit = { fg = c.border },
	TabLine = { fg = c.fg_dim, bg = c.bg_dark },
	TabLineFill = { bg = c.bg_dark },
	TabLineSel = { fg = c.fg_bright, bg = c.bg, bold = true },

	Pmenu = { fg = c.fg, bg = c.bg_dark },
	PmenuSel = { fg = c.bg, bg = c.cyan, bold = true },
	PmenuSbar = { bg = c.bg_light },
	PmenuThumb = { bg = c.fg_dim },
	WildMenu = { fg = c.bg, bg = c.cyan },

	Directory = { fg = c.cyan },
	Title = { fg = c.purple, bold = true },
	NonText = { fg = c.fg_dim },
	Whitespace = { fg = c.bg_light },
	EndOfBuffer = { fg = c.bg },
	Folded = { fg = c.fg_dim, bg = c.bg_dark, italic = true },
	FoldColumn = { fg = c.fg_dim },

	ErrorMsg = { fg = c.red, bold = true },
	WarningMsg = { fg = c.yellow, bold = true },
	MoreMsg = { fg = c.green },
	Question = { fg = c.cyan },
	ModeMsg = { fg = c.fg },

	-- Syntax
	Comment = { fg = c.fg_dim, italic = true },
	Constant = { fg = c.bright_magenta },
	String = { fg = c.green },
	Character = { fg = c.green },
	Number = { fg = c.bright_yellow },
	Boolean = { fg = c.bright_yellow },
	Float = { fg = c.bright_yellow },
	Identifier = { fg = c.fg_light },
	Function = { fg = c.cyan, bold = true },
	Statement = { fg = c.purple },
	Conditional = { fg = c.purple },
	Repeat = { fg = c.purple },
	Label = { fg = c.purple },
	Operator = { fg = c.blue },
	Keyword = { fg = c.purple, bold = true },
	Exception = { fg = c.red },
	PreProc = { fg = c.bright_cyan },
	Include = { fg = c.bright_cyan },
	Define = { fg = c.bright_cyan },
	Macro = { fg = c.bright_cyan },
	Type = { fg = c.blue },
	StorageClass = { fg = c.blue },
	Structure = { fg = c.blue },
	Typedef = { fg = c.blue },
	Special = { fg = c.cyan },
	SpecialChar = { fg = c.bright_cyan },
	Delimiter = { fg = c.fg_dim },
	Underlined = { underline = true },
	Ignore = { fg = c.fg_dim },
	Error = { fg = c.red, bold = true },
	Todo = { fg = c.bg, bg = c.yellow, bold = true },

	-- Diff
	DiffAdd = { fg = c.green, bg = c.bg_dark },
	DiffChange = { fg = c.yellow, bg = c.bg_dark },
	DiffDelete = { fg = c.red, bg = c.bg_dark },
	DiffText = { fg = c.cyan, bg = c.bg_dark, bold = true },

	-- Diagnostics
	DiagnosticError = { fg = c.red },
	DiagnosticWarn = { fg = c.yellow },
	DiagnosticInfo = { fg = c.blue },
	DiagnosticHint = { fg = c.cyan },
	DiagnosticOk = { fg = c.green },
	DiagnosticUnderlineError = { undercurl = true, sp = c.red },
	DiagnosticUnderlineWarn = { undercurl = true, sp = c.yellow },
	DiagnosticUnderlineInfo = { undercurl = true, sp = c.blue },
	DiagnosticUnderlineHint = { undercurl = true, sp = c.cyan },
	DiagnosticVirtualTextError = { fg = c.red, bg = c.bg_dark },
	DiagnosticVirtualTextWarn = { fg = c.yellow, bg = c.bg_dark },
	DiagnosticVirtualTextInfo = { fg = c.blue, bg = c.bg_dark },
	DiagnosticVirtualTextHint = { fg = c.cyan, bg = c.bg_dark },

	-- LSP
	LspReferenceText = { bg = c.sel_bg },
	LspReferenceRead = { bg = c.sel_bg },
	LspReferenceWrite = { bg = c.sel_bg },
	LspSignatureActiveParameter = { fg = c.cyan, bold = true },
	LspCodeLens = { fg = c.fg_dim, italic = true },

	-- Treesitter
	["@variable"] = { fg = c.fg_light },
	["@variable.builtin"] = { fg = c.bright_magenta, italic = true },
	["@variable.parameter"] = { fg = c.fg_light, italic = true },
	["@constant"] = { fg = c.bright_magenta },
	["@constant.builtin"] = { fg = c.bright_magenta, bold = true },
	["@string"] = { fg = c.green },
	["@string.escape"] = { fg = c.bright_cyan },
	["@function"] = { fg = c.cyan, bold = true },
	["@function.call"] = { fg = c.cyan },
	["@function.builtin"] = { fg = c.bright_blue },
	["@method"] = { fg = c.cyan },
	["@keyword"] = { fg = c.purple, bold = true },
	["@keyword.function"] = { fg = c.purple, bold = true },
	["@keyword.return"] = { fg = c.purple, bold = true },
	["@conditional"] = { fg = c.purple },
	["@repeat"] = { fg = c.purple },
	["@operator"] = { fg = c.blue },
	["@type"] = { fg = c.blue },
	["@type.builtin"] = { fg = c.blue, italic = true },
	["@property"] = { fg = c.fg_light },
	["@field"] = { fg = c.fg_light },
	["@parameter"] = { fg = c.fg_light, italic = true },
	["@punctuation.bracket"] = { fg = c.fg_dim },
	["@punctuation.delimiter"] = { fg = c.fg_dim },
	["@comment"] = { fg = c.fg_dim, italic = true },
	["@tag"] = { fg = c.purple },
	["@tag.attribute"] = { fg = c.bright_yellow },
	["@tag.delimiter"] = { fg = c.fg_dim },
	["@boolean"] = { fg = c.bright_yellow },
	["@number"] = { fg = c.bright_yellow },

	-- Git signs / gitgutter
	GitSignsAdd = { fg = c.green },
	GitSignsChange = { fg = c.yellow },
	GitSignsDelete = { fg = c.red },
	DiffAdded = { fg = c.green },
	DiffRemoved = { fg = c.red },

	-- Telescope
	TelescopeNormal = { fg = c.fg, bg = c.bg_dark },
	TelescopeBorder = { fg = c.border, bg = c.bg_dark },
	TelescopeSelection = { bg = c.sel_bg, bold = true },
	TelescopeMatching = { fg = c.cyan, bold = true },
	TelescopePromptBorder = { fg = c.cyan, bg = c.bg_dark },

	-- Nvim-tree / neo-tree
	NvimTreeNormal = { fg = c.fg, bg = c.bg_dark },
	NvimTreeFolderIcon = { fg = c.cyan },
	NvimTreeFolderName = { fg = c.fg_light },
	NvimTreeOpenedFolderName = { fg = c.cyan, bold = true },
	NvimTreeRootFolder = { fg = c.purple, bold = true },
	NvimTreeIndentMarker = { fg = c.fg_dim },
	NvimTreeGitDirty = { fg = c.yellow },
	NvimTreeGitNew = { fg = c.green },
	NvimTreeGitDeleted = { fg = c.red },
}

for group, opts in pairs(groups) do
	hl(0, group, opts)
end
