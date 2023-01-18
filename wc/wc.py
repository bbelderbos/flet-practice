from datetime import datetime

import pytz
import flet as ft
from worldclock import convert_time


def main(page: ft.Page):
    page.title = "World clock"
    now = datetime.now()

    def calculate_timezones(e):
        # TODO: should validate user input
        hour, minute = time.value.split(":")
        hour = int(hour)
        minute = int(minute)
        tzone = timezone.value
        output = convert_time(
            hour, minute, now.year, now.month, now.day, tzone)
        output = "\n".join(
            f"{time} in {zone}"
            for zone, time in output
        )
        result.value = output
        result.update()

    time = ft.TextField(label="Select time (HH:MM)")
    timezone = ft.Dropdown(
        options=[
            ft.dropdown.Option(tz)
            for tz in pytz.all_timezones
        ]
    )
    button = ft.ElevatedButton(
        "Calculate timezones",
        on_click=calculate_timezones)
    result = ft.Text()

    page.add(time, timezone, button, result)

ft.app(target=main)
