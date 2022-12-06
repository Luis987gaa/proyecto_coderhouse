import flet as ft
import httpx
import json
from ..components.appbar import app_bar

def login_view(page: ft.Page):

    _snack_bar = ft.SnackBar(content=ft.Text(''))

    def login_request(e, username, password):

        data = {
            "username": username,
            "password": password,
        }

        response = httpx.post('http://127.0.0.1:8000/api/user/auth/login/', json=data)
        data_str = response.content.decode('latin-1')
        data_dict: dict = json.loads(data_str)

        if response.status_code == 200:

            page.client_storage.set('user_id', data_dict['user_id'])
            page.client_storage.set('token', data_dict['token'])

            page.go('/')

        elif response.status_code == 400:
            _snack_bar.content = ft.Text(value=f"Error: Ups parece que tus datos son incorrectos.")

            if 'username' in data_dict.keys():
                _username_input.value = ""
                _username_input.error_text = data_dict['username'][0]

            if 'password' in data_dict.keys():
                _password_input.value = ""
                _password_input.error_text = data_dict['password'][0]

            if 'non_field_errors' in data_dict.keys():
                _username_input.value = ""
                _username_input.error_text = "Usuario inválido"
                _password_input.value = ""
                _password_input.error_text = "Contrasña invalida"
                _snack_bar.content = ft.Text(value=f"Error: {data_dict['non_field_errors'][0]}")

            _snack_bar.open = True
            page.update()

        elif response.status_code == 403:

            _username_input.value = ""
            _username_input.error_text = "Usuario inválido"
            _password_input.value = ""
            _password_input.error_text = "Contrasña invalida"
            _snack_bar.content = ft.Text(value="Error: Has alcanzado el maximo de sesiones iniciadas, si crees que es un error comunicate con el administrador. ")
            _snack_bar.open = True
            page.update()
        else:
            _snack_bar.content = ft.Text(f'Error {response.status_code} : {response.content.decode("latin-1")}')
            _snack_bar.open = True
            page.update()

    _username_input = ft.TextField(
        label='Nombre de usuario', border=ft.InputBorder.UNDERLINE)
    _password_input = ft.TextField(
        label='Contraseña', border=ft.InputBorder.UNDERLINE, password=True, can_reveal_password=True)

    _card = ft.Card(
        elevation=5,
        width=400,
        content=ft.Container(
            padding=30,
            content=ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        col=12,
                        controls=[
                            ft.Text(
                                value='Inicia sesion.',
                                style=ft.TextThemeStyle.HEADLINE_LARGE,
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ]
                    ),
                    ft.Column(
                        col=12,
                        controls=[
                            _username_input,
                            _password_input,
                        ]),
                    ft.Column(
                        col=6,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.TextButton(
                                'Registrate',
                                on_click=lambda e: page.go('/register')
                            ),
                        ]
                    ),
                    ft.Column(
                        col=6,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.TextButton(
                                'Inicia sesion',
                                on_click=lambda e: login_request(
                                    e,
                                    _username_input.value,
                                    _password_input.value,
                                )
                            ),
                        ]
                    )
                ]
            )
        )
    )

    _view = ft.View(
        appbar=app_bar(page),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            _card,
            _snack_bar,
        ]
    )

    return _view
