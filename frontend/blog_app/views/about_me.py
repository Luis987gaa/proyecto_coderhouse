import flet as ft
from ..components.appbar import app_bar


def about_me_view(page: ft.Page) -> ft.View:
    _view = ft.View(
        horizontal_alignment=ft.CrossAxisAlignment('center'),
        vertical_alignment=ft.MainAxisAlignment('center'),
        appbar=app_bar(page),
        controls=[
            ft.Card(
                elevation=5,
                content=ft.Container(
                    padding=50,
                    content=ft.ResponsiveRow(
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        width=600,
                        controls=[
                            ft.Column(
                                [
                                    ft.Image(
                                        src='img/user_img.jpg',
                                        height=200,
                                        border_radius=100,
                                    )
                                ],
                                col={
                                    'sm' : 12,
                                    'md' : 5
                                },
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        'Luis Fernando Charca Mamani',
                                        style=ft.TextThemeStyle.HEADLINE_LARGE,
                                        font_family='Milky'
                                    ),
                                    ft.Text(
                                        """Hola un gusto en saludarte, soy un estudiante de la salud, tengo 22 años y me gusta aprender nuevas cosas sin más te deseo un gran día y un komanta a la distancia""")

                                ],
                                col={
                                    'sm' : 12,
                                    'md' : 7
                                },
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            )
                        ]
                    )
                )
            )
        ]
    )

    return _view
