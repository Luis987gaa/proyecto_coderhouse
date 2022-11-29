import flet as ft
from ..components.navbar import NavBarComponent


class AboutMePage(ft.UserControl):

    def __init__(self, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    def build(self):

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        NavBarComponent(self.page),
                    ]
                )
            ]
        )