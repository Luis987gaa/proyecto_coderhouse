import flet as ft


class RegisterPage(ft.UserControl):
    _main_card = ft.Card(
        width=800,
        height=500,
        elevation=15,
    )

    _main_container = ft.Container(
        bgcolor=ft.colors.WHITE,
        border_radius=12,
    )

    _main_column = ft.Column(
        expand=True,
        horizontal_alignment='center'
    )

    _title_container_inputs = ft.Text(
        value='Registro de Usuario',
        weight='w200',
        style="displayMedium",
    )

    _container_inputs = ft.ResponsiveRow()

    _container_inputs_column_left = ft.Column(
        col={'lg': 6, 'md': 12},
        width=400,
        horizontal_alignment='center',
        expand=True
    )

    _container_inputs_column_right = ft.Column(
        col={'lg': 6, 'md': 12},
        width=400,
        horizontal_alignment='center',
        expand=True
    )

    # declaracion de los inputs.
    _username_field = ft.TextField(
        label='Username',
        border='underline',
        width=300,
    )

    _email_input = ft.TextField(
        label='Email',
        border='underline',
        width=300,
    )

    _name_input = ft.TextField(
        label='Nombres',
        border='underline',
        width=300,
    )

    _last_name_input = ft.TextField(
        label='Apellidos',
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
    _password_1_field = ft.TextField(
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
        text='Registrate')

    _login_btn = ft.FilledButton(
        text='Inicia Sesión')

    def __init__(self, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    def size_page_change(self, e):

        if self.page.width <= 750:
            self._main_card.height = 700
        else:
            self._main_card.height = 500
        self.update()

    def build(self):

        self._container_inputs_column_left.controls = [
            self._username_field,
            self._name_input,
            self._last_name_input,
        ]

        self._container_inputs_column_right.controls = [
            self._email_input,
            self._password_field,
            self._password_1_field,
        ]

        self._buttons_row.controls = [
            self._submit_btn,
            self._login_btn,
        ]

        self._container_inputs.controls = [
            self._container_inputs_column_left,
            self._container_inputs_column_right
        ]

        self._main_column.controls = [
            ft.Container(height=20),
            self._title_container_inputs,
            self._container_inputs,
            ft.Container(height=30),
            self._buttons_row
        ]

        self._main_container.content = self._main_column
        self._main_card.content = self._main_container
        self.page.on_resize = self.size_page_change
        return self._main_card




