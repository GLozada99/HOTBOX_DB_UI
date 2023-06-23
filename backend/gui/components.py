import re

from decouple import config
from nicegui import ui
from nicegui.elements.aggrid import AgGrid

from db.client import MongoDBClient
from db.config import get_config
from gui.callbacks import values_button_press_callback

REFRESH_TIME = 5


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


def flux_table_component():
    columns = [
        {
            "name": "time",
            "label": "Time",
            "field": "time",
            "required": True,
            "align": "left",
            "sortable": True,
        },
        {
            "name": "heat_flux_1",
            "label": "Heat Flux 1",
            "field": "heat_flux_1",
            "sortable": True,
        },
        {
            "name": "heat_flux_2",
            "label": "Heat Flux 2",
            "field": "heat_flux_2",
            "sortable": True,
        },
        {
            "name": "power_input",
            "label": "Power Input",
            "field": "power_input",
            "sortable": True,
        },
        {
            "name": "conductivity",
            "label": "Conductivity",
            "field": "conductivity",
            "sortable": True,
        },
    ]
    client = MongoDBClient(
        config("MONGO_USERNAME"),
        config("MONGO_PASSWORD"),
        config("MONGO_DBNAME"),
        "measurements",
    )

    def get_rows(client: MongoDBClient, quantity: int) -> list[dict]:
        with client:
            return [
                {
                    "time": entry["tiempo"],
                    "heat_flux_1": entry["Heat_flux_1"],
                    "heat_flux_2": entry["Heat_flux_2"],
                    "power_input": entry["Power_input"],
                    "conductivity": entry["conductivity"],
                }
                for entry in client.get_data_db(quantity)
            ]

    grid = ui.aggrid(
        {
            "columnDefs": columns,
            "rowData": get_rows(client, 8),
            "rowSelection": "multiple",
        }
    )

    def set_table_rows(grid: AgGrid, rows: list[dict]):
        print(rows)
        if grid.options["rowData"] != rows:
            grid.options["rowData"] = rows
            grid.update()

    ui.timer(REFRESH_TIME, lambda: set_table_rows(grid, get_rows(client, 8)))


def temperature_table_component():
    columns = [
        {
            "name": "temp_1",
            "label": "Temperature 1",
            "field": "temp_1",
        },
        {
            "name": "temp_2",
            "label": "Temperature 2",
            "field": "temp_2",
        },
        {
            "name": "temp_3",
            "label": "Temperature 3",
            "field": "temp_3",
        },
        {
            "name": "temp_4",
            "label": "Temperature 4",
            "field": "temp_4",
        },
        {
            "name": "temp_5",
            "label": "Temperature 5",
            "field": "temp_5",
        },
        {
            "name": "temp_6",
            "label": "Temperature 6",
            "field": "temp_6",
        },
        {
            "name": "temp_7",
            "label": "Temperature 7",
            "field": "temp_7",
        },
        {
            "name": "temp_8",
            "label": "Temperature 8",
            "field": "temp_8",
        },
        {
            "name": "temp_9",
            "label": "Temperature 9",
            "field": "temp_9",
        },
        {
            "name": "temp_10",
            "label": "Temperature 10",
            "field": "temp_10",
        },
    ]
    client = MongoDBClient(
        config("MONGO_USERNAME"),
        config("MONGO_PASSWORD"),
        config("MONGO_DBNAME"),
        "measurements",
    )

    def get_rows(client: MongoDBClient, quantity: int) -> list[dict]:
        with client:
            return [
                {
                    "temp_1": entry["temp_1"],
                    "temp_2": entry["temp_2"],
                    "temp_3": entry["temp_3"],
                    "temp_4": entry["temp_4"],
                    "temp_5": entry["temp_5"],
                    "temp_6": entry["temp_6"],
                    "temp_7": entry["temp_7"],
                    "temp_8": entry["temp_8"],
                    "temp_9": entry["temp_9"],
                    "temp_10": entry["temp_10"],
                }
                for entry in client.get_data_db(quantity)
            ]

    grid = ui.aggrid(
        {
            "columnDefs": columns,
            "rowData": get_rows(client, 8),
            "rowSelection": "multiple",
        }
    )

    def set_table_rows(grid: AgGrid, rows: list[dict]):
        print(rows)
        if grid.options["rowData"] != rows:
            grid.options["rowData"] = rows
            grid.update()

    ui.timer(REFRESH_TIME, lambda: set_table_rows(grid, get_rows(client, 8)))
