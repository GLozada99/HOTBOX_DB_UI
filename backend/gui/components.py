import re

from nicegui import ui

from db.config import get_config
from gui.callbacks import values_button_press_callback


def set_point_time_input_component():
    values = get_config()
    values_button = ui.button(
        "Set values",
        on_click=lambda _: values_button_press_callback(set_point_input, time_input),
    )
    set_point_input = ui.input(
        "Set Point (C°)",
        value=values["SETO_POINTO"],
        validation={
            "Must be a rational number": lambda v: bool(re.match(r"\d+\.*\d*", v)),
        },
    ).props("clearable")
    time_input = ui.input(
        "Time (S)",
        value=values["TIME"],
        validation={"Must be an integer": lambda v: bool(re.match(r"\d*", v))},
    ).props("clearable")
