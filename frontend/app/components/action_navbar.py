import flet as ft


class ActionsNavBar(ft.UserControl):

    def __init__(self, page: ft.Page, text: str, route: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.text: str = text
        self.route: str = route

    def on_hover_event(self, e):
        if e.control.content.color == "black":
            e.control.content.color = "white"
            e.control.content.update()
        else:
            e.control.content.color = "black"
            e.control.content.update()

    def on_click_actions(self, e):
        self.page.go(self.route)

    def build(self):
        _container = ft.Container(
            content=ft.Text(
                value=self.text,
                color='white',
                size=20,
                weight="w200",
            ),
            on_hover=lambda e: self.on_hover_event(e),
            on_click=lambda e: self.on_click_actions(e),
        )
        return _container