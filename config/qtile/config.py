# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["picom"])


def left_arrow(bg_color, fg_color):
    return widget.TextBox(
        text="\ue0b2", padding=0, fontsize=24, background=bg_color, foreground=fg_color
    )


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun -show-icons -b"), desc="Show launcher"),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer sset Master 5%-"),
        desc="Lower Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset Master 5%+"),
        desc="Raise Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer sset Master 1+ toggle"),
        desc="Mute/Unmute Volume",
    ),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [
    Group("\uf268"),  # Web
    Group("\uf121"),  # Dev
    Group("\ue86b"),  # Postman
    Group("\uf1c0"),  # Database
    Group("\uf1bc"),  # Music
    Group("\ueb4c"),  # Virtual Machine
]


for number, group in enumerate(groups, start=1):
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                str(number),
                lazy.group[group.name].toscreen(),
                desc=f"Switch to group {group.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(number),
                lazy.window.togroup(group.name, switch_group=True),
                desc=f"Switch to & move focused window to group {group.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Max(),
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="MesloLGS NF",
                    fontsize=18,
                    highlight_method="block",
                    this_current_screen_border="#875AE2",
                    active="#FFFFFF",
                    inactive="#787878",
                    rounded=False,
                    disable_drag=True,
                    borderwidth=14,
                ),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                left_arrow(bg_color="#000000", fg_color="#ffe26e"),
                widget.TextBox(
                    text="\uf4bc ",
                    background="#ffe26e",
                    foreground="#000000",
                    fontsize=16,
                ),
                widget.CPU(
                    background="#ffe26e",
                    format="{freq_current}GHz {load_percent}%",
                    foreground="#000000",
                    fmt="<b>{}</b> ",
                ),
                left_arrow(bg_color="#ffe26e", fg_color="#f29247"),
                widget.TextBox(
                    text="\uefc5 ",
                    background="#f29247",
                    foreground="#000000",
                    fontsize=14,
                ),
                widget.Memory(
                    background="#f29247", foreground="#000000", fmt="<b>{}</b> "
                ),
                left_arrow(bg_color="#f29247", fg_color="#f74646"),
                widget.TextBox(
                    text="\uf1eb ",
                    background="#f74646",
                    foreground="#000000",
                    fontsize=14,
                ),
                widget.Wlan(
                    interface="wlan0",
                    format="{essid}:",
                    disconnected_message="-",
                    foreground="000000",
                    background="f74646",
                ),
                widget.Net(
                    background="#f74646",
                    foreground="#000000",
                    fmt="<b>{}</b> ",
                    format="{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}",
                ),
                left_arrow(bg_color="#f74646", fg_color="#875AE2"),
                widget.TextBox(
                    text="\uf5ef",
                    background="#875AE2",
                    foreground="#000000",
                    fontsize=18,
                ),
                widget.Clock(
                    format="%Y/%m/%d - %I:%M %p",
                    background="#875AE2",
                    foreground="#000000",
                    fmt="<b>{}</b> ",
                ),
                left_arrow(bg_color="#875AE2", fg_color="#000000"),
                widget.TextBox(
                    text="Brayayin", background="#000000", foreground="#ffffff"
                ),
            ],
            26,
            border_width=[0, 0, 3, 0],  # Draw top and bottom borders
            border_color=[
                "000000",
                "000000",
                "000000",
                "000000",
            ],  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
        wallpaper="~/.config/qtile/wallpaper.png",
        wallpaper_mode="fill",
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="MesloLGS NF",
                    fontsize=18,
                    highlight_method="block",
                    this_current_screen_border="#875AE2",
                    active="#FFFFFF",
                    inactive="#787878",
                    rounded=False,
                    disable_drag=True,
                    borderwidth=14,
                ),
            ],
            26,
            border_width=[0, 0, 3, 0],  # Draw top and bottom borders
            border_color=[
                "000000",
                "000000",
                "000000",
                "000000",
            ],  # Borders are magenta
        ),
        wallpaper="~/.config/qtile/wallpaper.png",
        wallpaper_mode="fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
