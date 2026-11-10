#!/usr/bin/env python3
"""Write the WezTerm color schemes from the shared palette.

For each variant it writes plugin/kanagawa/schemes/<variant>.lua, which the
plugin loads, and themes/kanagawa-<variant>.toml, a scheme file for
`color_scheme_dirs`. Both hold the same colors.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
ANSI = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

# WezTerm color -> palette role. A tuple is a {bg, fg} pair of a tab style.
COLORS = {
    "background": "ui.bg",
    "foreground": "ui.fg",
    "cursor_bg": "ui.fg_dim",
    "cursor_fg": "ui.bg",
    "cursor_border": "ui.fg_dim",
    "selection_fg": "ui.fg",
    "selection_bg": "ui.bg_visual",
    "scrollbar_thumb": "ui.bg_p2",
    "split": "ui.nontext",
    "compose_cursor": "ui.special",
    "visual_bell": "ui.bg_p1",
}
# Colors that WezTerm takes as { Color = "..." }.
WRAPPED = {
    "copy_mode_active_highlight_bg": "ui.bg_visual",
    "copy_mode_active_highlight_fg": "ui.fg",
    "copy_mode_inactive_highlight_bg": "ui.bg_search",
    "copy_mode_inactive_highlight_fg": "ui.fg",
    "quick_select_label_bg": "diag.warning",
    "quick_select_label_fg": "term.black",
    "quick_select_match_bg": "ui.bg_search",
    "quick_select_match_fg": "ui.fg",
    "input_selector_label_bg": "ui.bg_p2",
    "input_selector_label_fg": "ui.fg",
    "launcher_label_bg": "ui.bg_p2",
    "launcher_label_fg": "ui.fg",
}
TAB_BAR = {"background": "ui.bg_m3", "inactive_tab_edge": "ui.nontext"}
# Tab style -> (bg role, fg role, italic).
TABS = {
    "active_tab": ("ui.bg_p2", "ui.fg", False),
    "inactive_tab": ("ui.bg_m3", "ui.fg_dim", False),
    "inactive_tab_hover": ("ui.bg_p1", "ui.fg", True),
    "new_tab": ("ui.bg_m3", "ui.fg_dim", False),
    "new_tab_hover": ("ui.bg_p1", "ui.fg", True),
}


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}


def lua(variant, c):
    q = lambda r: f'"{c[r]}"'  # noqa: E731
    out = [f'---@module "kanagawa.schemes.{variant}"', "", "---@type kanagawa.Scheme", "return {"]
    out += [f"  {k} = {q(r)}," for k, r in COLORS.items()]
    out += ["  ansi = {"] + [f'    "{c["term." + a]}",' for a in ANSI] + ["  },"]
    out += ["  brights = {"] + [f'    "{c["term.bright_" + a]}",' for a in ANSI] + ["  },"]
    out.append(f'  indexed = {{ [16] = {q("term.extended_1")}, [17] = {q("term.extended_2")} }},')
    out += [f"  {k} = {{ Color = {q(r)} }}," for k, r in WRAPPED.items()]
    out.append("  tab_bar = {")
    out += [f"    {k} = {q(r)}," for k, r in TAB_BAR.items()]
    for name, (bg, fg, italic) in TABS.items():
        out.append(f"    {name} = {{ bg_color = {q(bg)}, fg_color = {q(fg)}{', italic = true' if italic else ''} }},")
    out += ["  },", "}"]
    return "\n".join(out) + "\n"


def toml(variant, c):
    q = lambda r: f'"{c[r]}"'  # noqa: E731
    out = [
        "[metadata]",
        f'name = "Kanagawa {variant.capitalize()}"',
        'author = "Kanagawa Community"',
        'origin_url = "https://github.com/kanagawa-community/wezterm"',
        "",
        "[colors]",
    ]
    out += [f"{k} = {q(r)}" for k, r in COLORS.items()]
    out.append("ansi = [" + ", ".join(q("term." + a) for a in ANSI) + "]")
    out.append("brights = [" + ", ".join(q("term.bright_" + a) for a in ANSI) + "]")
    out += [f"{k} = {{ Color = {q(r)} }}" for k, r in WRAPPED.items()]
    out += ["", "[colors.indexed]", f'16 = {q("term.extended_1")}', f'17 = {q("term.extended_2")}', ""]
    out += ["[colors.tab_bar]"] + [f"{k} = {q(r)}" for k, r in TAB_BAR.items()] + [""]
    for name, (bg, fg, italic) in TABS.items():
        out += [f"[colors.tab_bar.{name}]", f"bg_color = {q(bg)}", f"fg_color = {q(fg)}"]
        out += ["italic = true"] if italic else []
        out.append("")
    return "\n".join(out)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        c = roles(variants[v])
        for out, text in (
            (ROOT / "plugin" / "kanagawa" / "schemes" / f"{v}.lua", lua(v, c)),
            (ROOT / "themes" / f"kanagawa-{v}.toml", toml(v, c)),
        ):
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text)
            print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
