---Minimal config for bug reports. Run it in isolation from your own config:
---
---    wezterm --config-file minit.lua
---
---Put your reproduction below the marker. Keep it as small as possible and
---paste the edited file into the bug report.
local wezterm = require "wezterm"
local kanagawa = wezterm.plugin.require "https://github.com/kanagawa-community/wezterm"
local config = wezterm.config_builder()

-- Edit below this line --------------------------------------------------------

kanagawa.apply_to_config(config)

return config
