from nicegui import ui

from gui.components import (
    set_point_time_input_component,
    flux_table_component,
    temperature_table_component,
    flux_graph_component,
    temperature_graph_component,
    conductivity_graph_component,
    start_box_component,
    isometric_view_component,
)


def main():
    with ui.row() as row:
        row.tailwind("justify-center")
        set_point_time_input_component()
        start_box_component()
        isometric_view_component()
    flux_table_component()
    temperature_table_component()
    flux_graph_component()
    temperature_graph_component()
    conductivity_graph_component()


if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run()
