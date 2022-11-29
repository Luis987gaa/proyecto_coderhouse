import flet as ft
import httpx
import json
from ..components.navbar import NavBarComponent
from ..components.post_min_card import PostMinComponent


class HomePage(ft.UserControl):

    _data_post: list = None
    _posts_list: list = []

    _column = ft.Column()

    def __init__(self, page: ft.Page, user: bool = False, user_data: dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.user = user
        self.user_data: dict = user_data

    def get_posts_backend(self):
        self._column.controls = []
        self._posts_list = []
        response = httpx.get('http://127.0.0.1:8000/api/posts/').content.decode('latin')
        self._data_post = json.loads(response)

    def get_posts_user_backend(self):
        self._column.controls = []
        self._posts_list = []
        self._data_post = []

        if self.user:
            headers = {
                'Authorization': f'Token {self.user_data["token"]}'
            }
            response = httpx.get(
                url=f'http://localhost:8000/api/posts/user/{self.user_data["user_id"]}',
                headers=headers
            ).content.decode('latin')
            print(response)
            self._data_post = json.loads(response)


    def build(self):

        if self.user:
            self.get_posts_user_backend()
        else:
            self.get_posts_backend()

        _posts_row = ft.ResponsiveRow(
            width=self.page.width * 0.75,
            spacing=20,
        )

        for post in self._data_post:
            _posts_row.controls.append(
                ft.Column(
                    col=6,
                    controls=[
                        PostMinComponent(
                            titulo=post['titulo'],
                            sub_titulo=post['sub_titulo'],
                            autor=post['autor']
                        )
                    ]
                )
            )

        _main_row = ft.Row(
            controls=[
                NavBarComponent(self.page),
            ]
        )

        return ft.Column(
            horizontal_alignment='center',
            controls=[
                _main_row,
                ft.Container(height=20),
                ft.Text(
                    value='Publicaciones',
                    style="displayLarge",
                ),
                ft.Container(height=20),
                _posts_row
            ]
        )
