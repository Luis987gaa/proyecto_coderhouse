import flet as ft
from .action_navbar import ActionsNavBar


class NavBarComponent(ft.UserControl):

    def __init__(self, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    # definicion del los widgets que conforman el navbar.
    _brand_container = ft.Container(
        padding=10
    )
    _brand_text = ft.Text(
        value="El Michi blog",
        size=40,
        font_family="Milky",
        color='white'
    )

    _actions_container = ft.Container()
    _actions_row = ft.Row(
        spacing=20
    )

    def on_hover_event(self, e):
        if e.control.content.color == "white":
            e.control.content.color = "black"
            e.control.content.update()
        else:
            e.control.content.color = "white"
            e.control.content.update()

    def redirect(self, e):
        self.page.go('/')

    def build(self):

        _brand_container = ft.Container(
            padding=12,
            content=self._brand_text,
            on_click=lambda e: self.redirect(e),
            on_hover=lambda e: self.on_hover_event(e),
        )

        self._actions_row.controls = [
            ActionsNavBar(self.page, 'Mis Publicaciones', '/mis-posts'),
            ActionsNavBar(self.page, 'Sobre Mí', '/about-me'),
            ActionsNavBar(self.page, 'Inicio de sesion', '/login'),
            ActionsNavBar(self.page, 'Registro', '/register'),
            ActionsNavBar(self.page, 'Cerrar Sesion', '/logout'),
        ]

        self._actions_container.content = self._actions_row

        self._brand_container.on_hover = lambda e: self.on_hover_event(e)

        return ft.Column(
            controls=[
                ft.Row(
                    width=self.page.width * 0.95,
                    alignment='spaceBetween',
                    controls=[
                        _brand_container,
                        self._actions_container,
                    ]
                )
            ]
        )
