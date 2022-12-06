import flet as ft

class PostMinComponent(ft.UserControl):
    _main_card = ft.Card(
        elevation=5,
    )

    _main_container = ft.Container(
        border_radius=12,
        width=500,
        padding=10,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):

        self._main_container.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=500,
                    controls=[
                        ft.Text(
                            value=self.data['titulo'],
                            style=ft.TextThemeStyle.TITLE_LARGE,
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=500,
                    height=50,
                    controls=[
                        ft.Text(
                            value=f' - {self.data["sub_titulo"]}',
                            style=ft.TextThemeStyle.BODY_MEDIUM,
                        )
                    ]
                ),
                ft.Image(
                    src=self.data["image_post"],
                    height=150
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=400,
                    controls=[
                        ft.Text(
                            value=f'Publicado por - {self.data["autor"]}',
                            style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        ft.TextButton(
                            text='Ver más...',
                            on_click=lambda e: self.page.go(f'/post/{self.data["id"]}')
                        )
                    ]
                ),
            ]
        )

        self._main_card.content = self._main_container
        return self._main_card
