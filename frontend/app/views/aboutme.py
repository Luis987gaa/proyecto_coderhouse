import flet as ft
from ..components.navbar import NavBarComponent


class AboutMePage(ft.UserControl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        return ft.Column(
            controls=[
                ft.Row(controls=[
                    NavBarComponent(self.page),
                    ft.Text('Esta es la about me page')
                ]
                )
            ]
        )