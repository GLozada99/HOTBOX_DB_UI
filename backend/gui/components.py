import re

from decouple import config
from nicegui import ui
from nicegui.elements.aggrid import AgGrid

# from box.main import box_main
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


def start_box_component():
    values = get_config()
    values_button = ui.button(
        "Start",
        on_click=lambda _: None,
        # on_click=lambda _: box_main(),
    )


def isometric_view_component():
    with ui.card().tight() as card:
        ui.image(
            f"https://cdn.discordapp.com/attachments/366674772408533013/1122650766566490152/Isometrica.jpeg"
        )
        with ui.card_section():
            ui.label("Explode and Isometric Hotbox Design View")


def flux_table_component():
    columns = [
        {
            "field": "time",
            "headerName": "Time",
            "sortable": True,
            "resizable": True,
        },
        {
            "field": "heat_flux_1",
            "headerName": "Heat Flux 1 (W/m2)",
            "sortable": True,
            "resizable": True,
        },
        {
            "field": "heat_flux_1",
            "headerName": "Heat Flux 2 (W/m2)",
            "sortable": True,
            "resizable": True,
        },
        {
            "field": "power_input",
            "headerName": "Power Input (W)",
            "sortable": True,
            "resizable": True,
        },
        {
            "field": "conductivity",
            "headerName": "Conductivity (W/m-k)",
            "sortable": True,
            "resizable": True,
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
                    "heat_flux_1": "%.2f" % entry["Heat_flux_1"],
                    "heat_flux_2": "%.2f" % entry["Heat_flux_2"],
                    "power_input": "%.2f" % entry["Power_input"],
                    "conductivity": "%.5f" % entry["conductivity"],
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
        if grid.options["rowData"] != rows:
            grid.options["rowData"] = rows
            grid.update()

    ui.timer(REFRESH_TIME, lambda: set_table_rows(grid, get_rows(client, 8)))


def temperature_table_component():
    columns = [
        {
            "headerName": "T1 (C°)",
            "label": "Temperature 1",
            "field": "temp_1",
            "resizable": True,
        },
        {
            "headerName": "T2 (C°)",
            "label": "Temperature 2",
            "field": "temp_2",
            "resizable": True,
        },
        {
            "headerName": "T3 (C°)",
            "label": "Temperature 3",
            "field": "temp_3",
            "resizable": True,
        },
        {
            "headerName": "T4 (C°)",
            "label": "Temperature 4",
            "field": "temp_4",
            "resizable": True,
        },
        {
            "headerName": "T5 (C°)",
            "label": "Temperature 5",
            "field": "temp_5",
            "resizable": True,
        },
        {
            "headerName": "T6 (C°)",
            "label": "Temperature 6",
            "field": "temp_6",
            "resizable": True,
        },
        {
            "headerName": "T7 (C°)",
            "label": "Temperature 7",
            "field": "temp_7",
            "resizable": True,
        },
        {
            "headerName": "T8 (C°)",
            "label": "Temperature 8",
            "field": "temp_8",
            "resizable": True,
        },
        {
            "headerName": "T9 (C°)",
            "label": "Temperature 9",
            "field": "temp_9",
            "resizable": True,
        },
        {
            "headerName": "T10 (C°)",
            "label": "Temperature 10",
            "field": "temp_10",
            "resizable": True,
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
                    "temp_1": "%.2f" % entry["temp_1"],
                    "temp_2": "%.2f" % entry["temp_2"],
                    "temp_3": "%.2f" % entry["temp_3"],
                    "temp_4": "%.2f" % entry["temp_4"],
                    "temp_5": "%.2f" % entry["temp_5"],
                    "temp_6": "%.2f" % entry["temp_6"],
                    "temp_7": "%.2f" % entry["temp_7"],
                    "temp_8": "%.2f" % entry["temp_8"],
                    "temp_9": "%.2f" % entry["temp_9"],
                    "temp_10": "%.2f" % entry["temp_10"],
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
        if grid.options["rowData"] != rows:
            grid.options["rowData"] = rows
            grid.update()

    ui.timer(REFRESH_TIME, lambda: set_table_rows(grid, get_rows(client, 8)))


def flux_graph_component():
    line_plot = ui.line_plot(
        n=2, limit=7200, figsize=(14, 7), update_every=1
    ).with_legend(["Heat Flux 1", "Heat Flux 2"], loc="upper center", ncol=2)
    count = 0

    def update_line_plot(rows: list[dict]) -> None:
        nonlocal count
        for row in rows:
            x = count
            count += 1
            y1 = row["heat_flux_1"]
            y2 = row["heat_flux_2"]
            line_plot.push([x], [[y1], [y2]])
            line_plot.fig.gca().set_ylim(150, 300)
            line_plot._convert_to_html()

    def get_rows(client: MongoDBClient, quantity: int) -> list[dict]:
        with client:
            return [
                {
                    "time": entry["tiempo"],
                    "heat_flux_1": entry["Heat_flux_1"],
                    "heat_flux_2": entry["Heat_flux_2"],
                }
                for entry in client.get_data_db(quantity)
            ]

    client = MongoDBClient(
        config("MONGO_USERNAME"),
        config("MONGO_PASSWORD"),
        config("MONGO_DBNAME"),
        "measurements",
    )
    line_updates = ui.timer(
        1, lambda: update_line_plot(get_rows(client, 1)), active=True
    )


def temperature_graph_component():
    line_plot = ui.line_plot(
        n=2, limit=7200, figsize=(14, 7), update_every=1
    ).with_legend(["Hot Side Avg", "Cold Side Avg"], loc="upper center", ncol=2)

    count = 0

    def update_line_plot(rows: list[dict]) -> None:
        nonlocal count
        for row in rows:
            x = count
            count += 1
            y1 = sum(row["hot"]) / len(row["hot"])
            y2 = sum(row["cold"]) / len(row["cold"])
            line_plot.push([x], [[y1], [y2]])
            line_plot.fig.gca().set_ylim(0, 85)
            line_plot._convert_to_html()

    def get_rows(client: MongoDBClient, quantity: int) -> list[dict]:
        with client:
            return [
                {
                    "hot": [
                        entry["temp_1"],
                        entry["temp_2"],
                        entry["temp_3"],
                        entry["temp_4"],
                        entry["temp_5"],
                        entry["temp_6"],
                        entry["temp_7"],
                        entry["temp_8"],
                    ],
                    "cold": [
                        entry["temp_9"],
                        entry["temp_10"],
                    ],
                }
                for entry in client.get_data_db(quantity)
            ]

    client = MongoDBClient(
        config("MONGO_USERNAME"),
        config("MONGO_PASSWORD"),
        config("MONGO_DBNAME"),
        "measurements",
    )
    line_updates = ui.timer(
        1, lambda: update_line_plot(get_rows(client, 1)), active=True
    )


def conductivity_graph_component():
    line_plot = ui.line_plot(
        n=1, limit=7200, figsize=(14, 7), update_every=1
    ).with_legend(["Conductivity"], loc="upper center", ncol=1)
    count = 0

    def update_line_plot(rows: list[dict]) -> None:
        nonlocal count
        for row in rows:
            x = count
            count += 1
            y1 = row["conductivity"]
            line_plot.push([x], [[y1]])
            line_plot.fig.gca().set_ylim(0, 1)
            line_plot._convert_to_html()

    def get_rows(client: MongoDBClient, quantity: int) -> list[dict]:
        with client:
            return [
                {
                    "conductivity": entry["conductivity"],
                }
                for entry in client.get_data_db(quantity)
            ]

    client = MongoDBClient(
        config("MONGO_USERNAME"),
        config("MONGO_PASSWORD"),
        config("MONGO_DBNAME"),
        "measurements",
    )
    line_updates = ui.timer(
        1, lambda: update_line_plot(get_rows(client, 1)), active=True
    )
