#!/usr/bin/python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import codecs
import json
import plistlib
import re
import glob
from os import remove
# Created by aziz (SyncedSidebarbg)
# Modified by xxxzc


class MatchColorScheme(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        global cache
        if view.settings().get('is_widget') or \
                view.settings().get('theme') is None:
            return
        if "Fits" not in view.settings().get('theme'):
            # print("[Theme-Fits] Activated only use Fits.sublime-theme")
            return

        scheme_file = view.settings().get('color_scheme')
        if not scheme_file or scheme_file == cache.get('color_scheme'):
            return

        # read scheme file to get current color settings
        plist_file = plistlib.readPlistFromBytes(
            sublime.load_resource(scheme_file).encode('utf-8'))
        global_settings = [i["settings"] for i in plist_file[
            "settings"] if i["settings"].get("lineHighlight")]
        color_settings = global_settings and global_settings[0]
        hightlight = [i["settings"] for i in plist_file[
            "settings"] if "string" in str(i.get("scope")) or
            "constant" in str(i.get("scope"))]
        hightlight = hightlight and hightlight[0]
        if not color_settings or not hightlight:
            return  # can't find

        cache = {"color_scheme": scheme_file}

        bg = color_settings.get("background", '#FFFFFF').lower()
        fg = color_settings.get("foreground", '#000000').lower()
        hl = hightlight.get("foreground", '#FFFFFF').lower()  # hightlight

        # hex color to rgb color mapping
        _NUMERALS = '0123456789abcdef'
        _HEXDEC = {v: int(v, 16)
                   for v in (x + y for x in _NUMERALS for y in _NUMERALS)}

        # convert hex color to rgb color list [r, g, b]
        def hex_to_rgb(hex_color):
            lens = len(hex_color)
            if lens == 7 or lens == 9:  # '#123456' or '#ff123456'
                hex_list = re.findall(r".{2}", hex_color[-6:])
            elif lens == 4:  # '#abc'
                hex_list = [i * 2 for i in hex_color[1:]]
            return list(map(lambda x: _HEXDEC[x], hex_list))

        # get color brightness
        def brightness(rgb):
            return ((rgb[0] * 299) + (rgb[1] * 587) + (rgb[2] * 114)) // 1000

        colors = {}

        def rgb_and_yiq(hex_color):
            tup = colors.setdefault(hex_color, [hex_to_rgb(hex_color), -1])
            if tup[1] == -1:
                tup[1] = brightness(tup[0])
            return tup

        # color with mask

        class Mode:
            bg = 0  # background
            ft = 1  # font
            li = 2  # line

        def color(mode=-1, arg=0, c=bg):
            if mode == Mode.bg:  # background mode
                [rgb, yiq] = rgb_and_yiq(c)
                # default mask is to deeper
                arg = -arg
                if yiq == 0:
                    arg = 0  # darkness
                elif yiq < 10:
                    arg = -arg  # to light
                elif yiq > 180:
                    arg *= 4  # to deeper

            if mode == Mode.li:
                [rgb, yiq] = rgb_and_yiq(c)
                if arg == 0:
                    arg = 20
                if yiq < 30:
                    arg = 25
                    rgb = [255, 255, 255]
                else:
                    rgb = [0, 0, 0]

            if mode == Mode.ft:  # font mode
                yiq = rgb_and_yiq(bg)[1]
                if c == bg:
                    c = fg
                rgb = hex_to_rgb(c)
                if yiq > 127:  # background is light
                    arg = -arg + 20

            if mode == Mode.li:  # opacity mode
                rgb.append(arg)
            else:
                rgb = [max(min(x + arg, 255), 0) for x in rgb]

            return rgb

        template = [
            # tab
            {
                "class": "tabset_control",
                "layer0.tint": color(Mode.bg, 5),
                "layer1.tint": color(Mode.li)
            },
            {
                "class": "tab_control",
                "layer0.tint": color(Mode.bg, 5),
                "layer1.tint": color(Mode.li)
            },
            {
                "class": "tab_control", "attributes": ["selected"],
                "layer0.tint": color(Mode.bg),
                "layer1.tint": color(Mode.li, 50)
            },
            # tab_label
            {
                "class": "tab_label",
                "fg": color(Mode.ft, -50)
            },
            {
                "class": "tab_label",
                "parents": [{"class": "tab_control",
                             "attributes": ["selected"]}],
                "fg": color(Mode.ft)
            },
            # close button
            {
                "class": "tab_close_button",
                "layer0.tint": color(Mode.ft)
            },
            {
                "class": "tab_close_button",
                "parents": [{"class": "tab_control",
                             "attributes": ["selected"]}],
                "layer1.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "show_tabs_dropdown_button",
                "layer0.tint": color(Mode.ft)
            },
            {
                "class": "panel_close_button",
                "layer0.tint": color(Mode.ft)
            },
            {
                "class": "close_button",
                "layer0.tint": color(Mode.ft)
            },
            # status bar
            {
                "class": "status_bar",
                "layer0.tint": color(Mode.bg),
                "layer0.opacity": 1,
                "layer1.tint": color(Mode.li)
            },
            {
                "class": "panel_button_control",
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 0.75
            },
            {
                "class": "panel_button_control",
                "attributes": ["hover"],
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 0.75
            },
            {
                "class": "label_control",
                "color": color(Mode.ft, -50)
            },
            {
                "class": "overlay_control",
                "layer0.tint": color(Mode.bg)
            },
            {
                "class": "popup_control",
                "layer0.tint": color(Mode.bg)
            },
            {
                "class": "mini_quick_panel_row",
                "layer0.tint": color(Mode.bg)
            },
            {
                "class": "tool_tip_control",
                "layer0.tint": color(Mode.bg)
            },
            {
                "class": "tool_tip_label_control",
                "color": color(Mode.ft)
            },
            # auto complete
            {
                "class": "auto_complete",
                "layer0.tint": color(Mode.bg)
            },
            {
                "class": "auto_complete_label",
                "fg": color(Mode.ft, -50),
                "match_fg": color(Mode.ft, -30),
                "selected_fg": color(Mode.ft, 10),
                "selected_match_fg": color(Mode.ft, 20)
            },
            # crtl+shift+p
            {
                "class": "mini_quick_panel_row",
                "attributes": ["selected"],
                "layer1.tint": color(Mode.li, 20),
            },
            {
                "class": "quick_panel_label",
                "fg": color(Mode.ft, -50),
                "match_fg": color(Mode.ft, -30, hl),
                "selected_fg": color(Mode.ft, 10),
                "selected_match_fg": color(Mode.ft, 20, hl)
            },
            {
                "class": "quick_panel_path_label",
                "fg": color(Mode.ft),
                "match_fg": color(Mode.ft),
                "selected_fg": color(Mode.ft),
                "selected_match_fg": color(Mode.ft)
            },
            {
                "class": "panel_control",
                "layer0.tint": color(Mode.bg),
                "layer1.tint": color(Mode.li),
            },
            {
                "class": "panel_button_control",
                "layer0.tint": color(Mode.ft)
            },
            # scroll bar
            {
                "class": "scroll_bar_control",
                "layer0.tint": color(Mode.bg),
            },

            {
                "class": "disclosure_button_control",
                "layer0.tint": color(Mode.ft),
                "layer1.tint": color(Mode.ft)
            },
            # side bar
            {
                "class": "tree_row",
                "layer0.tint": color(Mode.bg)
            },
            {
                "class": "tree_row",
                "attributes": ["selected"],
                "layer0.tint": color(Mode.bg),
                "layer1.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "sidebar_tree",
                "layer0.tint": color(Mode.bg, 5),
                "layer0.opacity": 1,
                "layer2.tint": color(Mode.li),
            },
            {
                "class": "sidebar_label",
                "color": color(Mode.ft),
            },
            {
                "class": "sidebar_label",
                "parents": [{"class": "tree_row"}],
                "color": color(Mode.ft, -50)
            },
            {
                "class": "sidebar_label",
                "parents": [{"class": "tree_row",
                             "attributes": ["selected"]}],
                "color": color(Mode.ft)
            },
            {
                "class": "sidebar_heading",
                "color": color(Mode.ft, 0, hl),
            },
            # icon set
            {
                "class": "icon_folder",
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 0.75
            },
            {
                "class": "icon_file_type",
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 0.75
            },
            {
                "class": "icon_folder_loading",
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 0.5
            },
            {
                "class": "icon_folder_dup",
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 1
            },
            {
                "class": "icon_regex",
                "layer0.tint": color(Mode.ft),
            },
            {
                "class": "icon_regex",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "icon_case",
                "layer0.tint": color(Mode.ft),
            },
            {
                "class": "icon_case",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "icon_whole_word",
                "layer0.texture": "Theme - Fits/Fits/icons/wholeword.png",
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 1,
                "content_margin": 8
            },
            {
                "class": "icon_whole_word",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },

            {
                "class": "icon_context",
                "layer0.texture": "Theme - Fits/Fits/icons/context.png",
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 1,
                "content_margin": 8
            },
            {
                "class": "icon_context",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },

            {
                "class": "icon_use_buffer",
                "layer0.texture": "Theme - Fits/Fits/icons/buffer.png",
                "layer0.tint": color(Mode.ft),
                "layer0.opacity": 1,
                "content_margin": 8
            },
            {
                "class": "icon_use_buffer",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "icon_reverse",
                "layer0.tint": color(Mode.ft),
            },
            {
                "class": "icon_reverse",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "icon_wrap",
                "layer0.tint": color(Mode.ft),
            },
            {
                "class": "icon_wrap",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "icon_in_selection",
                "layer0.tint": color(Mode.ft),
            },
            {
                "class": "icon_in_selection",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "icon_preserve_case",
                "layer0.tint": color(Mode.ft),
            },
            {
                "class": "icon_preserve_case",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },
            {
                "class": "icon_highlight",
                "layer0.tint": color(Mode.ft),
            },
            {
                "class": "icon_highlight",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": color(Mode.ft, 0, hl)
            },
        ]

        json_str = json.dumps(template, sort_keys=True, indent=4, separators=(
            ',', ': ')).encode('raw_unicode_escape')
        global new_theme_file_path
        new_theme_file_path  = sublime.packages_path() + "/User/" + \
            view.settings().get('theme')
        with codecs.open(new_theme_file_path, 'w', 'utf-8') as f:
            f.write(json_str.decode())


def plugin_loaded():
    global cache
    cache = {}


def plugin_unloaded():
    return
