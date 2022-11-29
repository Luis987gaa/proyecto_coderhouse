import flet as ft

class PostMinComponent(ft.UserControl):

    _main_card = ft.Card(
        elevation=15,
    )

    _main_container = ft.Container(
        border_radius=12,
        height=150,
        width=500,
        padding=10
    )

    def __init__(self, titulo, sub_titulo, autor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.titulo = titulo
        self.sub_titulo = sub_titulo
        self.autor = autor

    def build(self):

        self._main_container.content = ft.Column(
            horizontal_alignment="center",
            controls=[
                ft.Row(
                    alignment="center",
                    width=500,
                    controls=[
                        ft.Text(
                            value=self.titulo,
                            style="titleLarge",
                        ),
                    ]
                ),
                ft.Row(
                    alignment="center",
                    width=500,
                    height=50,
                    controls=[
                        ft.Text(
                            value=f' - {self.sub_titulo}',
                            style="bodyMedium",
                        )
                    ]
                ),
                ft.Row(
                    alignment="spaceBetween",
                    width=400,
                    controls=[
                        ft.Text(
                            value=f'Publicado por - {self.autor}',
                            style="labelMedium",
                        ),
                        ft.TextButton(
                            text='Ver más...'
                        )
                    ]
                ),
            ]
        )

        self._main_card.content = self._main_container
        return self._main_card

