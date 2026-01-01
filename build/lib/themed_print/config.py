# -*- coding: utf-8 -*-
"""
Created on 2026-01-01 20:06:32

@author: Yiheng Yu
"""

from rich.theme import Theme

DEFAULT_THEME = Theme(
    inherit=True,
    styles={
        "CONSTANT": "#ff9b54",
        "STR": "sea_green2 bold",
        "NUMBER": "sky_blue1 bold",
        "TRUE": "#C5D86D bold",
        "FALSE": "#D8829D bold",
        "DICT_KEY": "#94a3b8 bold",
        "PUNCTUATION": "grey39",
        "ENUM": "#cdb4db",
        "NONE": "#ffbd00 bold",
        "DATACLASS_NAME": "#c77dff",
        "HOUR": "dark_slate_gray1",
        "MINUTE": "dark_slate_gray1",
        "SECOND": "dark_slate_gray1",
        "FUNCTION_NAME": "green1 bold",
        "INSTANCE_CLS": "medium_spring_green",
        "CLASS": "gold3 bold",
        "MODULE": "orange3",
        "MODULE_FROM": "orange3",
        "HEX_ADDRESS": "dodger_blue1",
    },
)