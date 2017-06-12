#!/usr/bin/python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import codecs
import json
import plistlib
import glob
from os import path, remove

# Created by aziz (SyncedSidebarbg)
# Modified by xxxzc


class MatchColorScheme(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        global cache
        if view.settings().get('theme') is None:
            return
        if view.settings().get('theme') != "Fits.sublime-theme":
            print("Theme-Fits will be activated only use Fits.sublime-theme")
            artifacts = path.join(sublime.packages_path(),
                                  "User", "Fits.sublime-theme")
            for f in glob.glob(artifacts):
                remove(f)
            return
        scheme_file = view.settings().get('color_scheme')
        # do nothing if it's a widget
        if view.settings().get('is_widget'):
            return
        # do nothing if the sheme file is not available or the same as before
        if not scheme_file or scheme_file == cache.get('color_scheme'):
            return
        plist_file = plistlib.readPlistFromBytes(
            sublime.load_resource(scheme_file).encode('utf-8'))
        global_settings = [i["settings"] for i in plist_file[
            "settings"] if i["settings"].get("lineHighlight")]
        color_settings = global_settings and global_settings[0]
        constant_dict = [i["settings"] for i in plist_file[
            "settings"] if "string" in str(i.get("scope")) or
            "constant" in str(i.get("scope"))]
        constant_dict = constant_dict and constant_dict[0]
        if not color_settings:
            return
        if not constant_dict:
            return
        bg = color_settings.get("background", '#FFFFFF')
        fg = color_settings.get("foreground", '#000000')
        hl = constant_dict.get("foreground", '#FFFFFF')  # hightlight
        bgc = bg.lstrip('#')
        cache = {"bg": bg, "fg": fg, "color_scheme": scheme_file}

        # -- COLOR ------------------------------

        _NUMERALS = '0123456789abcdefABCDEF'
        _HEXDEC = {v: int(v, 16)
                   for v in (x + y for x in _NUMERALS for y in _NUMERALS)}

        def rgb(triplet):
            return _HEXDEC[triplet[0:2]], \
                _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]

        def is_light(triplet):
            r, g, b = _HEXDEC[triplet[0:2]], _HEXDEC[
                triplet[2:4]], _HEXDEC[triplet[4:6]]
            yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000
            return yiq >= 128

        def color_variant(hex_color, brightness_offset=1):
            if len(hex_color) == 9:
                print("=> Passed %s into color_variant()" % hex_color)
                hex_color = hex_color[0:-2]
                print("=> Reformatted as %s " % hex_color)
            if len(hex_color) != 7:
                raise Exception(
                    "Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
            rgb_hex = [hex_color[x:x + 2] for x in [1, 3, 5]]
            new_rgb_int = [int(hex_value, 16) +
                           brightness_offset for hex_value in rgb_hex]
            # make sure new values are between 0 and 255
            new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
            return "#%02x%02x%02x" % tuple(new_rgb_int)

        # --------------------------------------

        def with_brightness(bg, brightness_change=50):
            if is_light(bg.lstrip('#')):
                return rgb(color_variant(bg, -1 * brightness_change).lstrip('#'))
            else:
                return rgb(color_variant(bg, brightness_change).lstrip('#'))

        def use_color(bg):
            return rgb(bg.lstrip('#'))

        template = [
            {
                "class": "tab_close_button",
                "parents": [{"class": "tab_control", "attributes": ["selected"]}],
                "layer1.tint": use_color(hl)
            },
            {
                "class": "tab_close_button",
                "parents": [{"class": "tab_control", "attributes": ["dirty"]}],
                "layer1.tint": use_color(hl)
            },
            {
                "class": "tool_tip_control",
                "layer0.tint": use_color(bg)
            },
            {
                "class": "tool_tip_label_control",
                "color": with_brightness(bg, 160)
            },
            {
                "class": "panel_close_button",
                "layer0.tint": with_brightness(fg, 0)
            },
            {
                "class": "close_button",
                "layer0.tint": with_brightness(fg, 0)
            },
            {
                "class": "tab_close_button",
                "layer0.tint": with_brightness(hl, 0)
            },
            {
                "class": "tab_close_button",
                "parents": [{"class": "tab_control", "attributes": ["dirty", "hover"]}],
                "layer0.tint": with_brightness(fg, 0)
            },
            {
                "class": "show_tabs_dropdown_button",
                "layer0.tint": with_brightness(fg, 0)
            },
            {
                "class": "show_tabs_dropdown_button",
                "attributes": ["hover"],
                "layer0.tint": with_brightness(hl, 0)
            },
            {
                "class": "status_bar",
                "layer0.tint": use_color(bg),
                "layer0.opacity": 1
            },
            {
                "class": "overlay_control",
                "layer0.tint": use_color(bg)
            },
            {
                "class": "popup_control",
                "layer0.tint": use_color(bg)
            },
            {
                "class": "mini_quick_panel_row",
                "layer0.tint": with_brightness(bg, 0)
            },
            {
                "class": "auto_complete",
                "layer0.tint": use_color(bg)
            },
            {
                "class": "auto_complete_label",
                "fg": with_brightness(bg, 110),
                "match_fg": with_brightness(bg, 160),
                "selected_fg": with_brightness(bg, 150),
                "selected_match_fg": with_brightness(bg, 255)
            },
            {
                "class": "quick_panel_label",
                "fg": with_brightness(fg, 0),
                "match_fg": with_brightness(hl, 50),
                "selected_fg": with_brightness(fg, 0),
                "selected_match_fg": with_brightness(hl, 0)
            },
            {
                "class": "mini_quick_panel_row",
                "attributes": ["selected"],
                "layer1.tint": with_brightness(bg, 30),
            },
            {
                "class": "quick_panel_path_label",
                "fg": with_brightness(bg, 90),
                "match_fg": with_brightness(bg, 200),
                "selected_fg": with_brightness(bg, 120),
                "selected_match_fg": with_brightness(bg, 255)
            },
            {
                "class": "label_control",
                "color": with_brightness(fg, 0)
            },
            {
                "class": "panel_control",
                "layer0.tint": use_color(bg),
            },
            {
                "class": "panel_button_control",
                "layer0.tint": with_brightness(fg, 0)
            },
            {
                "class": "scroll_bar_control",
                "layer0.tint": use_color(bg),
            },
            {
                "class": "tab_control", "attributes": ["selected"],
                "layer2.tint": with_brightness(fg, 0)
            },

            {
                "class": "disclosure_button_control",
                "layer0.tint": with_brightness(fg),
                "layer1.tint": with_brightness(fg)
            },
            {
                "class": "tree_row",
                "layer0.tint": with_brightness(bg, 0)
            },
            {
                "class": "tree_row",
                "attributes": ["selected"],
                "layer0.tint": use_color(bg),
                "layer1.tint": use_color(hl)
            },
            {
                "class": "sidebar_tree",
                "layer0.tint": with_brightness(bg, 0),
                "layer0.opacity": 1,
                "dark_content": not is_light(bgc)
            },
            # {
            #     "class": "sidebar_container",
            #     "layer0.tint": with_brightness(bg, 30),
            # },
            {
                "class": "sidebar_label",
                "color": with_brightness(fg, 30),
            },
            {
                "class": "sidebar_label",
                "parents": [{"class": "tree_row"}],
                "color": with_brightness(fg, 30)
            },
            {
                "class": "sidebar_label",
                "parents": [{"class": "tree_row", "attributes": ["selected"]}],
                "color": with_brightness(fg, 0)
            },
            {
                "class": "sidebar_heading",
                "color": with_brightness(fg, 0),
            },

            {
                "class": "icon_folder",
                "layer0.tint": with_brightness(fg, 50)
            },
            {
                "class": "icon_file_type",
                "layer0.tint": with_brightness(fg, 0)
            },
            {
                "class": "icon_folder_loading",
                "layer0.tint": with_brightness(fg, 0)
            },
            {
                "class": "icon_folder_dup",
                "layer0.tint": with_brightness(fg, 0)
            },
            {
                "class": "icon_regex",
                "layer0.tint": with_brightness(fg, 0),
            },
            {
                "class": "icon_regex",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },
            {
                "class": "icon_case",
                "layer0.tint": with_brightness(fg, 0),
            },
            {
                "class": "icon_case",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },
            {
                "class": "icon_whole_word",
                "layer0.texture": "Theme - Fits/Fits/icons/wholeword.png",
                "layer0.tint": with_brightness(fg, 0),
                "layer0.opacity": 1,
                "content_margin": 8
            },
            {
                "class": "icon_whole_word",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },

            {
                "class": "icon_context",
                "layer0.texture": "Theme - Fits/Fits/icons/context.png",
                "layer0.tint": with_brightness(fg, 0),
                "layer0.opacity": 1,
                "content_margin": 8
            },
            {
                "class": "icon_context",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },

            {
                "class": "icon_use_buffer",
                "layer0.texture": "Theme - Fits/Fits/icons/buffer.png",
                "layer0.tint": with_brightness(fg, 0),
                "layer0.opacity": 1,
                "content_margin": 8
            },
            {
                "class": "icon_use_buffer",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },
            {
                "class": "icon_reverse",
                "layer0.tint": with_brightness(fg, 0),
            },
            {
                "class": "icon_reverse",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },
            {
                "class": "icon_wrap",
                "layer0.tint": with_brightness(fg, 0),
            },
            {
                "class": "icon_wrap",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },
            {
                "class": "icon_in_selection",
                "layer0.tint": with_brightness(fg, 0),
            },
            {
                "class": "icon_in_selection",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },
            {
                "class": "icon_preserve_case",
                "layer0.tint": with_brightness(fg, 0),
            },
            {
                "class": "icon_preserve_case",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },
            {
                "class": "icon_highlight",
                "layer0.tint": with_brightness(fg, 0),
            },
            {
                "class": "icon_highlight",
                "parents": [{"class": "icon_button_control", "attributes": ["selected"]}],
                "layer0.tint": use_color(hl)
            },
        ]

        json_str = json.dumps(template, sort_keys=True, indent=4, separators=(
            ',', ': ')).encode('raw_unicode_escape')
        new_theme_file_path = sublime.packages_path() + "/User/" + \
            view.settings().get('theme')
        with codecs.open(new_theme_file_path, 'w', 'utf-8') as f:
            f.write(json_str.decode())


def plugin_loaded():
    global cache
    cache = {}


def plugin_unloaded():
    artifacts = path.join(sublime.packages_path(), "User", "*.sublime-theme")
    for f in glob.glob(artifacts):
        remove(f)
