#!/usr/bin/python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import codecs
import json
import plistlib
import re
import glob
import random
from os import remove

# Created by aziz (SyncedSidebarbg)
# Modified by xxxzc


class Adapter(sublime_plugin.EventListener):
    def on_load_async(self, view):
        if cache.get('mode', 'active') == "passive":
            self.adapting(view)
        return

    def on_activated_async(self, view):
        if cache.get('mode', 'active') == "active":
            self.adapting(view)
        return

    def adapting(self, view): # normal mode
        global cache
        if view.settings().get('is_widget') or \
                view.settings().get('theme') is None or \
           "Fits.sublime-theme" != view.settings().get('theme'):
            return
        scheme_file = view.settings().get('color_scheme')
        if not scheme_file:
            return

        settings = sublime.load_settings("Fits.sublime-settings")
        cache['mode'] = settings.get('mode')

        settingAccent = settings.get('accent').lower()

        if scheme_file == cache.get('color_scheme') and \
            cache['scope'] == settings.get('scope') and \
            (cache['accent'] == settingAccent or \
                (settingAccent == "" and cache['accent'] == cache['theme_accent'])):
            return

        # read scheme file to get current color settings
        plist_file = plistlib.readPlistFromBytes(sublime.load_resource(scheme_file).encode('utf-8'))

        global_settings = [i["settings"] for i in plist_file[
            "settings"] if i.get('settings', False) and i["settings"].get("caret")]
        color_settings = global_settings and global_settings[0]
        cache['background'] = color_settings.get('background', "#888").lower()
        cache['foreground'] = color_settings.get('foreground', "#888").lower()

        cache['scope'] = settings.get('scope')
        accent = [i["settings"] for i in plist_file[
            "settings"] if cache['scope'] in str(i.get("scope"))]
        cache["theme_accent"] =  accent and accent[0] \
                                    and accent[0].get("foreground").lower()
        cache["accent"] = cache["theme_accent"] if settingAccent == "" else settingAccent

        cache["color_scheme"] = scheme_file

        # hex color to rgb color mapping
        _NUMERALS = '0123456789abcdef'
        _HEXDEC = {v: int(v, 16)
                   for v in (x + y for x in _NUMERALS for y in _NUMERALS)}

        # convert hex color to rgb color list [r, g, b]
        def hex_to_rgb(hex_color):
            lens = len(hex_color)
            if lens == 7:  # '#123456'
                hex_list = re.findall(r".{2}", hex_color[-6:])
            elif lens == 4:  # '#abc'
                hex_list = [i * 2 for i in hex_color[1:]]
            return list(map(lambda x: _HEXDEC[x], hex_list))

        # get color brightness
        def brightness(rgb):
            return ((rgb[0] * 299) + (rgb[1] * 587) + (rgb[2] * 114)) // 1000

        def rgb_and_yiq(hex_color):
            rgb = hex_to_rgb(hex_color)
            return rgb, brightness(rgb)

        bg, dark = rgb_and_yiq(cache.get('background'))
        fg, light= rgb_and_yiq(cache.get("foreground"))
        hl = hex_to_rgb(cache.get("accent"))

        black = [0, 0, 0]
        white = [255, 255, 255]
        BG, FG, HL = 0, 1, 2
        def color(mode=0, op=0, rev=False):
            if mode != HL:
                if dark < 30:
                    if mode == FG:
                        op = 30 - op
                        op *= 3
                    elif mode == BG:
                        op /= 1.5
                mask = white
                if mode == BG and dark > 30: 
                    mask = black
                if mode == FG and light > 150 and dark > 30:
                    mask = black
                if rev: 
                    print(dark)
                    mask = white if dark < 130 else black
            else:
                mask = hl
                if op == 0: op = 100
            color = "background" if mode == BG else "foreground"
            return [color] + mask + [op/100]


        sep_line_color = color(BG, 20)
        panel_btn_color = color(BG, 3, True)
        bar_mask_color = color(BG, 10)
        foreground = color(FG)
        background = color()
        accent = color(HL)

        template = [
            # side bar
            {
                "class": "sidebar_container",
                "layer0.tint": sep_line_color,
            },
            {
                "class": "sidebar_tree",
                "layer0.tint": color(BG, 5)
            },
            {
                "class": "tree_row",
                "layer0.tint": color(BG, 15),
                "layer1.tint": color(HL, 75)
            },
            {
                "class": "sidebar_heading",
                "fg": accent
            },
            {
                "class": "sidebar_label",
                "color": color(FG, 5)
            },
            {
                "class": "sidebar_label",
                "parents": [{"class": "tree_row",
                             "attributes": ["selected"]}],
                "color": color(HL, 75)
            },
            {
                "class": "close_button",
                "layer0.tint": foreground
            },
            # tab
            {
                "class": "tabset_control",
                "layer0.tint": bar_mask_color,
                "layer1.tint": sep_line_color
            },
            {
                "class": "tab_control",
                "layer0.tint": bar_mask_color,
                "layer1.tint": sep_line_color,
            },
            {
                "class": "tab_control", "attributes": ["selected"],
                "layer0.tint": background
            },
            # tab_label
            {
                "class": "tab_label",
                "fg": color(FG, 20)
            },
            {
                "class": "tab_label",
                "parents": [{"class": "tab_control",
                             "attributes": ["selected"]}],
                "fg": color(HL, 20)
            },
            # close button
            {
                "class": "tab_close_button",
                "layer0.tint": foreground
            },
            {
                "class": "tab_close_button",
                "parents": [{"class": "tab_control",
                             "attributes": ["selected"]}],
                "layer1.tint": accent
            },
            {
                "class": "tab_close_button",
                "parents": [{"class": "tab_control",
                             "attributes": ["dirty"]}],
                "layer1.tint": color(HL, 80)
            },
            {
                "class": "show_tabs_dropdown_button",
                "layer0.tint": color(FG, 40)
            },
            # quick panel
            {
                "class": "overlay_control",
                "layer0.tint": bar_mask_color
            },
            {
                "class": "quick_panel",
                "layer0.tint": bar_mask_color
            },
            {
                "class": "quick_panel_row",
                "layer0.tint": panel_btn_color
            },
            {
                "class": "mini_quick_panel_row",
                "layer0.tint": panel_btn_color
            },
            {
                "class": "quick_panel_label",
                "fg": color(FG, 20),
                "match_fg": color(FG, 5),
                "selected_fg": foreground,
                "selected_match_fg": accent
            },
            {
                "class": "quick_panel_path_label",
                "fg": color(FG, 20),
                "match_fg": color(FG, 20),
                "selected_fg": foreground,
                "selected_match_fg": foreground
            },

            # views
            {
                "class": "grid_layout_control",
                "border_color": sep_line_color,
                "border_size": 1
            },
            {
                "class": "minimap_control",
                "viewport_color": color(BG, 15),
            },
            { # code folding button
                "class": "fold_button_control",
                "layer0.tint": foreground
            },
            { # auto complete
                "class": "popup_control",
                "layer0.tint": color(BG, 5)
            },
            {
                "class": "auto_complete",
                "layer0.tint": background
            },
            {
                "class": "auto_complete_label",
                "fg": color(FG, 10), 
                "match_fg": color(FG, 5),
                "selected_fg": foreground,
                "selected_match_fg": accent
            },
            {
                "class": "table_row",
                "layer0.tint": color(BG, 15)
            },

            # panel
            {
                "class": "panel_control",
                "layer0.tint": bar_mask_color,
                "layer1.tint": sep_line_color,
            },
            {
                "class": "panel_close_button",
                "layer0.tint": foreground
            },

            # dialog
            { 
                "class": "dialog",
                "layer0.tint": background
            },
            {
                "class": "progress_bar_control",
                "layer0.tint": foreground
            },
            {
                "class": "progress_gauge_control",
                "layer0.tint": accent
            },

            # scroll bar
            {
                "class": "scroll_bar_control",
                "layer0.tint": background,
            },
            {
                "class": "puck_control",
                "attributes": ["horizontal"],
                "layer0.tint": foreground,
            },

            # input
            {
                "class": "text_line_control",
                "layer0.tint": panel_btn_color,
                "color_scheme_tint": panel_btn_color
            },
            {
                "class": "dropdown_button_control",
                "layer0.tint": foreground
            }, 

            # button
            {
                "class": "button_control",
                "layer0.tint": panel_btn_color
            },
            {
                "class": "icon_button_control",
                "layer0.tint": panel_btn_color
            },

            # label
            {
                "class": "label_control",
                "fg": color(FG, 10),
            },
            { # info
                "class": "title_label_control",
                "fg": foreground
            },

            # tool tip
            {
                "class": "tool_tip_control",
                "layer0.tint": color(BG),
                "layer1.tint": sep_line_color
            },
            {
                "class": "tool_tip_label_control",
                "fg": foreground
            },

            # status bar
            {
                "class": "status_bar",
                "layer0.tint": bar_mask_color,
                "layer1.tint": sep_line_color
            },
            {
                "class": "panel_button_control",
                "layer0.tint": color(FG, 30)
            },
            {
                "class": "status_button",
                "layer0.tint": color(BG, 20)
            },

            # icon set
            {
                "class": "icon_folder",
                "layer0.tint": foreground,
                "layer0.opacity": 0.75
            },
            {
                "class": "icon_folder_loading",
                "layer0.tint": foreground,
                "layer0.opacity": 0.75
            },
            {
                "class": "icon_folder_dup",
                "layer0.tint": foreground,
                "layer0.opacity": 0.75
            },
            {
                "class": "icon_file_type",
                "layer0.tint": foreground,
                "layer0.opacity": 0.75
            },
            {
                "class": "icon_file_type",
                "parents": [{"class": "tree_row",
                             "attributes": ["selected"]}],
                "layer0.tint": accent,
                "layer0.opacity": 0.75
            },
            {
                "class": "icon_regex",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_regex",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },
            {
                "class": "icon_case",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_case",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },
            {
                "class": "icon_whole_word",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_whole_word",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },

            {
                "class": "icon_context",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_context",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },

            {
                "class": "icon_use_buffer",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_use_buffer",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },
            {
                "class": "icon_reverse",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_reverse",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },
            {
                "class": "icon_wrap",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_wrap",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },
            {
                "class": "icon_in_selection",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_in_selection",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },
            {
                "class": "icon_preserve_case",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_preserve_case",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            },
            {
                "class": "icon_highlight",
                "layer0.tint": foreground,
            },
            {
                "class": "icon_highlight",
                "parents": [{"class": "icon_button_control",
                             "attributes": ["selected"]}],
                "layer0.tint": accent
            }
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
