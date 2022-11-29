import flet as ft
from ..components.navbar import NavBarComponent


class NotFoundPage(ft.UserControl):

    _text = ft.Text(
        value="""404: Opps. La Página que buscas no existe.""",
        text_align='center',
        style='displayLarge'
    )

    def __init__(self, page: ft.Page, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    def build(self):
        return ft.Column(
            horizontal_alignment="center",
            controls=[
                NavBarComponent(self.page),
                ft.Row(
                    width=self.page.width,
                    height=self.page.height * 0.75,
                    alignment="center",
                    controls=[
                        ft.Container(
                            width=self.page.width * 0.50,
                            content=self._text
                        )
                    ]
                )
            ]
        )
