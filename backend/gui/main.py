from nicegui import ui

from gui.components import set_point_time_input_component


def main():
    set_point_time_input_component()


if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run()
