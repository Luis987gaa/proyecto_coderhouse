import flet as ft
import httpx
import json
from ..components.appbar import app_bar


def register_view(page: ft.Page):

    _snack_bar = ft.SnackBar(content=ft.Text(''))

    def register_request(e, name, last_name, email, username, password, repeat_password):

        data = {
            'name': name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': password,
            'password2': repeat_password,
        }

        response = httpx.post('http://127.0.0.1:8000/api/user/register/', json=data)

        if response.status_code == 201:
            _name_input.value = ""
            _last_name_input.value = ""
            _username_input.value = ""
            _username_input.error_text = ""
            _email_input.value = ""
            _email_input.error_text = ""
            _password_input.value = ""
            _password_input.error_text = ""
            _repeat_password_input.value = ""
            _repeat_password_input.error_text = ""

            _snack_bar.content = ft.Text(value=f'Exito: {name} te registraste correctamente ya puedes iniciar sesion.')
            _snack_bar.open = True

            page.update()

        elif response.status_code == 400:
            data_str = response.content.decode('latin-1')
            data_dict: dict = json.loads(data_str)

            if 'username' in data_dict.keys():
                _username_input.value = ""
                _username_input.error_text = data_dict['username'][0]

            if 'email' in data_dict.keys():
                _email_input.value = ""
                _email_input.error_text = data_dict['email'][0]

            if 'password' in data_dict.keys():
                _password_input.value = ""
                _password_input.error_text = data_dict['password'][0]

            if 'password2' in data_dict.keys():
                _repeat_password_input.value = ""
                _repeat_password_input.error_text = data_dict['password2'][0]

            _snack_bar.content = ft.Text(value='Error: Los datos ingresados son invalidos.')
            _snack_bar.open = True
            page.update()

        else:
            _snack_bar.content = ft.Text(f'Error {response.status_code} : {response.content.decode("latin-1")}')
            _snack_bar.open = True
            page.update()

    _name_input = ft.TextField(
        label='Nombre', border=ft.InputBorder.UNDERLINE)
    _last_name_input = ft.TextField(
        label='Apellidos', border=ft.InputBorder.UNDERLINE)
    _email_input = ft.TextField(
        label='Correo', border=ft.InputBorder.UNDERLINE)
    _username_input = ft.TextField(
        label='Nombre de usuario', border=ft.InputBorder.UNDERLINE)
    _password_input = ft.TextField(
        label='Contraseña', border=ft.InputBorder.UNDERLINE, password=True, can_reveal_password=True)
    _repeat_password_input = ft.TextField(
        label='Repite Contraseña', border=ft.InputBorder.UNDERLINE, password=True, can_reveal_password=True)

    _card = ft.Card(
        elevation=5,
        width=500,
        content=ft.Container(
            padding=30,
            content=ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        col=12,
                        controls=[
                            ft.Text(
                                value='Registro',
                                style=ft.TextThemeStyle.HEADLINE_LARGE,
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ]
                    ),
                    ft.Column(
                        col={
                            "md": 6,
                            "sm": 12
                        },
                        controls=[
                            _name_input,
                            _last_name_input,
                            _email_input
                        ]),
                    ft.Column(
                        col={
                            "md": 6,
                            "sm": 12
                        },
                        controls=[
                            _username_input,
                            _password_input,
                            _repeat_password_input,
                        ]),
                    ft.Column(
                        col=6,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.TextButton(
                                'Inicia sesion',
                                on_click=lambda e: page.go('/login')

                            ),
                        ]
                    ),
                    ft.Column(
                        col=6,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.TextButton(
                                'Registrate',
                                on_click=lambda e: register_request(
                                    e,
                                    _name_input.value,
                                    _last_name_input.value,
                                    _email_input.value,
                                    _username_input.value,
                                    _password_input.value,
                                    _repeat_password_input.value,
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
            _snack_bar
        ]
    )

    return _view
