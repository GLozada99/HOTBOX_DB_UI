import datetime

from nicegui import ui
from nicegui.elements.input import Input
from nicegui.elements.line_plot import LinePlot

from db.config import set_config


def values_button_press_callback(set_point_input: Input, time_input: Input):
    try:
        if (set_point := float(set_point_input.value)) > 70:
            ui.notify(
                "Set Point value is recommended to be less than 70 C°", type="warning"
            )
    except ValueError:
        ui.notify(
            f"Set Point does not have a correct value ({set_point_input.value})",
            type="negative",
        )
        return

    try:
        if (time := int(time_input.value)) < 7200:
            ui.notify("Time value is recommended to be at least 2700 s", type="warning")
    except ValueError:
        ui.notify(
            f"Time does not have a correct value ({time_input.value})", type="negative"
        )
        return

    set_config(set_point, time)


def save_graph_callback(line_plot: LinePlot, name: str):
    now = str(datetime.datetime.now())
    line_plot.fig.savefig(f"./images/{name} {now}.jpg", format='jpg')
    ui.notify(f"{name} was saved successfully", type="positive")
