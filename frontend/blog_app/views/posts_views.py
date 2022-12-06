import flet as ft
import httpx
import json
from ..components.appbar import app_bar
from ..components.post_min_card import PostMinComponent


class PostResponsive(ft.UserControl):
    _controls_responsive: list = []
    _responsive_row = ft.ResponsiveRow()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_post = None

    def get_data(self):
        response = httpx.get('http://127.0.0.1:8000/api/posts/').content.decode('latin')

        return json.loads(response)

    def did_mount(self):

        dict_data = self.get_data()

        if not dict_data:
            self._responsive_row.controls = [
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    col=12,
                    controls=[
                        ft.Row(
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Image(
                                    'img/no-no.gif',
                                    width=100,
                                ),
                                ft.Text(
                                    ' Se ha publicado nada aún...',
                                    style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                )
                            ]
                        )

                    ]
                )
            ]
            self.update()
        else:

            self._controls_responsive.clear()

            for post in dict_data:
                self._controls_responsive.append(
                    ft.Column(
                        col={'sm': 12, 'md': 6},
                        controls=[
                            PostMinComponent(data=post),
                        ]
                    )
                )
            self._responsive_row.controls = self._controls_responsive
            self.update()

    def build(self):

        self._responsive_row.controls = [
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                col=12,
                controls=[
                    ft.ProgressRing(width=16, height=16, stroke_width=2)
                ]
            )
        ]

        return self._responsive_row


def posts_view(page: ft.Page):
    _posts = PostResponsive()

    _view = ft.View(
        appbar=app_bar(page),
        scroll=ft.ScrollMode.HIDDEN,
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        col=12,
                        controls=[
                            ft.Text(
                                value='Mi Blog',
                                style=ft.TextThemeStyle.DISPLAY_LARGE,
                                text_align=ft.TextAlign.CENTER,
                                font_family='Milky'
                            ),
                            ft.Text(
                                value='Aqui encontraras las publicaciones posteadas por el usuario.',
                                style=ft.TextThemeStyle.HEADLINE_LARGE,
                                text_align=ft.TextAlign.CENTER,
                            )
                        ]),
                    ft.Column(col={'sm': 12, 'md': 2}, controls=[]),
                    ft.Column(col={'sm': 12, 'md': 8}, controls=[_posts]),
                    ft.Column(col={'sm': 12, 'md': 2}, controls=[]),
                ]
            ),

        ]
    )

    return _view
