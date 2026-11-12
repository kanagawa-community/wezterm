# Window hook for .github/scripts/capture-windows.sh: WezTerm runs the shared session
# from docs/PREVIEWS.md with each theme.
# It loads the TOML scheme, which holds the same colors as the plugin.
# Requires: wezterm, fastfetch, eza.
# shellcheck shell=bash
name=WezTerm

launch() {
  cat >"$work/wezterm-$1.lua" <<LUA
return {
  color_scheme_dirs = { "$root/themes" },
  color_scheme = "Kanagawa ${1^}",
  font = require("wezterm").font("$font"),
  font_size = 11,
  enable_wayland = true,
  use_fancy_tab_bar = false,
  hide_tab_bar_if_only_one_tab = false,
  window_decorations = "NONE",
  window_padding = { left = 8, right = 8, top = 8, bottom = 8 },
}
LUA
  printf 'wezterm --config-file %s start -- %s %s' "$work/wezterm-$1.lua" "$session" "$1"
}
