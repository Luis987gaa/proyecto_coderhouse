import flet as ft
from ..components.appbar import app_bar


def not_found_view(page: ft.Page) -> ft.View:
    _view = ft.View(
        horizontal_alignment=ft.CrossAxisAlignment('center'),
        vertical_alignment=ft.MainAxisAlignment('center'),
        appbar=app_bar(page),
        controls=[
            ft.Image(
                src='/img/no_page_found.png'
            )
        ]
    )

    return _view
