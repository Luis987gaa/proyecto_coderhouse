import flet as ft
from typing import Dict
import httpx
import json
from datetime import datetime
from ..components.appbar import app_bar
from ..components.post_min_card import PostMinComponent


class MyPostsResponsive(ft.UserControl):

    _controls_responsive: list = []
    _responsive_row = ft.ResponsiveRow()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self):
        headers = httpx.Headers(
            {"Authorization": f"Token {self.data['token']}",
             "Content-Type": "application/json"})

        response = httpx.get(
            f'http://127.0.0.1:8000/api/posts/user/{self.data["user_id"]}', headers=headers)

        # TODO: Manejo de errores 403 No Authorizaded

        data_str = response.content.decode('latin-1')
        return json.loads(data_str)

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
                                    ' haz publicado nada aún...',
                                    style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                    text_align=ft.TextAlign.START,
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
                            ft.Container(
                                content=PostMinComponent(data=post),
                                on_click=lambda e: self.page.go(f'/post/{post["id"]}')
                            )
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


def my_posts_view(page: ft.Page):
    token = page.client_storage.get('token')
    user_id = page.client_storage.get('user_id')

    _my_posts = MyPostsResponsive(data={
        'token': token,
        'user_id': user_id
    })

    _text_inpup_titulo = ft.TextField(
        label='Titulo'
    )
    _text_inpup_subtitulo = ft.TextField(
        label='Sub Titulo'
    )
    _text_inpup_contenido = ft.TextField(
        label='Contenido',
        multiline=True
    )

    _card_post_register = ft.Card(visible=False)

    _container_post_register = ft.Container(
        padding=20
    )

    _container_post_register.content = ft.Column(controls=[
        _text_inpup_titulo,
        _text_inpup_subtitulo,
        _text_inpup_contenido,
        ft.TextButton(text='Guardar', icon=ft.icons.SAVE, on_click=lambda e: request_register(e)),
    ])

    _card_post_register.content = _container_post_register

    def request_register(e):
        data = {
            "titulo": _text_inpup_titulo.value,
            "sub_titulo": _text_inpup_subtitulo.value,
            "contenido": _text_inpup_contenido.value,
            "autor": user_id,
            "image_post": "img/no_image.png"
        }
        headers = httpx.Headers(
            {"Authorization": f"Token {token}",
             "Content-Type": "application/json"})

        print(data)
        print(headers)
        response = httpx.post('http://127.0.0.1:8000/api/post/create', json=data ,headers=headers)

        if response.status_code == 201:
            _text_inpup_titulo.value = ""
            _text_inpup_subtitulo.value = ""
            _text_inpup_contenido.value = ""
            _text_inpup_titulo.error_text = ""
            _text_inpup_subtitulo.error_text = ""
            _text_inpup_contenido.error_text = ""
            _card_post_register.update()

            _my_posts.did_mount()
        elif response.status_code == 400:
            data_str = response.content.decode('latin-1')
            data_dict: dict = json.loads(data_str)
            if 'titulo' in data_dict.keys():
                _text_inpup_titulo.value = ""
                _text_inpup_titulo.error_text = data_dict['titulo'][0]

            if 'sub_titulo' in data_dict.keys():
                _text_inpup_subtitulo.value = ""
                _text_inpup_subtitulo.error_text = data_dict['sub_titulo'][0]

            if 'contenido' in data_dict.keys():
                _text_inpup_contenido.value = ""
                _text_inpup_contenido.error_text = data_dict['contenido'][0]

        elif response.status_code == 403:
            page.go('/not-authorized')

        _view.update()

    def open_form_register(e):
        _card_post_register.visible = True
        _card_post_register.update()

    _view = ft.View(
        appbar=app_bar(page),
        scroll=ft.ScrollMode.HIDDEN,
        controls=[
            ft.ResponsiveRow(

                controls=[
                    ft.Column(col=12, height=30),
                    ft.Column(
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        col=12,
                        controls=[
                            ft.Text(
                                value='Mis publicaiones.',
                                style=ft.TextThemeStyle.DISPLAY_LARGE,
                                text_align=ft.TextAlign.CENTER,
                                font_family='Milky'
                            ),
                        ]),

                    ft.Column(col={'sm': 12, 'md': 4}, controls=[]),
                    ft.Column(col={'sm': 12, 'md': 4},
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              controls=[
                                  ft.TextButton(
                                      text='Publicar algo',
                                      icon=ft.icons.ADD,
                                      on_click=lambda e: open_form_register(e)
                                  ),
                                  _card_post_register,
                              ]),
                    ft.Column(col={'sm': 12, 'md': 4}, controls=[]),

                    ft.Column(col={'sm': 12, 'md': 2}, controls=[]),
                    ft.Column(col={'sm': 12, 'md': 8},
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                              controls=[_my_posts]),
                    ft.Column(col={'sm': 12, 'md': 2}, controls=[]),
                ]
            ),

        ]
    )

    return _view
