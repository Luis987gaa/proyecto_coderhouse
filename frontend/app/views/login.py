import json

import flet as ft
import httpx

class LoginPage(ft.UserControl):

    def __init__(self, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    _main_card = ft.Card(
        elevation=15,
    )

    _main_container = ft.Container(
        bgcolor=ft.colors.WHITE,
        border_radius=12,
    )

    _row = ft.Row(
        vertical_alignment='center',
    )

    _container_inputs = ft.Container()

    _title_container_inputs = ft.Text(
        value='Inicio de sesión',
        weight='w200',
        style="displayMedium",
    )

    _container_inputs_column = ft.Column(
        width=700,
        horizontal_alignment='center',
        expand=True
    )

    _username_field = ft.TextField(
        label='Nombre de usuario',
        border='underline',
        width=300,
    )

    _password_field = ft.TextField(
        label='Contraseña',
        border='underline',
        password=True,
        can_reveal_password=True,
        width=300,
    )

    _buttons_row = ft.Row(
        width=500,
        alignment="center"
    )

    _submit_btn = ft.FilledButton(
        text='Inicia sesion')

    _register_btn = ft.FilledButton(
        text='Registrate')

    # image container
    _container_image = ft.Container(
        image_fit='fill'
    )

    _image_log = ft.Image(
        src='/login.jpg',
        border_radius=12,
    )

    _dialog = ft.AlertDialog()

    def req_login(self, e, username: str, password: str):

        data = {
            "username": username,
            "password": password
        }

        response = httpx.post('http://127.0.0.1:8000/api/user/auth/login/', json=data)

        if response.status_code == 200:

            """ cuando se inicio correctamente de sesion. """
            data_str = response.content.decode('latin')

            self.page.client_storage.set('credentials', data_str)
            self.page.go('/')

        elif response.status_code == 400:
            """ cuando los datos enviados son incorrectos. """
            self._username_field.error_text = 'Nombre de usuario incorrecto.'
            self._username_field.value = ""
            self._password_field.error_text = 'Contraseña incorrecta.'
            self._password_field.value = ""
            self.update()

        elif response.status_code == 403:
            """ cuando hay demasiadas sesiones iniciadas. """
            self._dialog.title = ft.Text(
                value='Ups:Tienes demasiadas sesiones iniciadas.',
                color='red'
            )
            self._dialog.open = True
            self.update()

    def size_page_change(self, e):
        if self.page.width < 750:

            self._row.controls = [
                self._container_inputs
            ]

        else:
            self._row.controls = [
                self._container_image,
                self._container_inputs
            ]
        self.update()

    def build(self):

        self._submit_btn.on_click = lambda e: self.req_login(
            e,
            self._username_field.value,
            self._password_field.value
        )

        self._register_btn.on_click = lambda e: self.page.go('/register')

        self._buttons_row.controls = [
            self._submit_btn,
            self._register_btn,
        ]

        self._container_inputs_column.controls = [
            ft.Container(height=10),
            self._title_container_inputs,
            self._username_field,
            self._password_field,
            ft.Container(height=10),
            self._buttons_row,
            self._dialog,
        ]

        self._container_inputs.content = self._container_inputs_column

        self._container_image.content = self._image_log

        if self.page.width < 750:

            self._row.controls = [
                self._container_inputs
            ]

        else:
            self._row.controls = [
                self._container_image,
                self._container_inputs,
            ]

        self._main_container.content = self._row
        self._main_card.content = self._main_container

        # evento de redimecionado de la pagina.
        self.page.on_resize = self.size_page_change

        return self._main_card

