import flet as ft
import httpx


def app_bar(page: ft.Page) -> ft.AppBar:

    _user_actions = ft.PopupMenuButton(
        content=ft.Text('Mi perfil')
    )

    def user_actions():
        if page.client_storage.contains_key('token') or page.client_storage.contains_key('user_id'):
            _user_actions.items =[
                ft.PopupMenuItem(
                    icon=ft.icons.LOGOUT,
                    text='Cerrar Sesión',
                    on_click=lambda e: log_out(e))
            ]

        else:
            _user_actions.items = [
                ft.PopupMenuItem(
                    icon=ft.icons.LOGIN,
                    text='Iniciar Sesión',
                    on_click=lambda e: page.go('/login')
                ),
                ft.PopupMenuItem(
                    icon=ft.icons.APP_REGISTRATION,
                    text='Registrarse',
                    on_click=lambda e: page.go('/register'),
                ),
            ]

    def log_out(e):

        _user_actions.disabled = True
        _user_actions.update()
        token = page.client_storage.get('token')

        headers = {'Authorization': f'Token {token}'}
        response = httpx.post('http://127.0.0.1:8000/api/user/auth/logoutall/', headers=headers)

        # TODO: aplicacion de mensajeria de session  finalizada.

        page.client_storage.clear()

        user_actions()
        _user_actions.disabled = False
        _user_actions.update()
        page.go('/')

    user_actions()

    _app_bar = ft.AppBar(
        leading_width=300,
        elevation=10,
        toolbar_height=50,
        leading=ft.Container(
            padding=10,
            content=ft.Container(
                ft.Text(
                    'Mi blog',
                    size=20,
                    font_family='Milky'
                ),
            ),
            on_click=lambda e: page.go('/')
        ),
        actions=[
            ft.Row(
                spacing=20,
                controls=[
                    ft.PopupMenuButton(
                        content=ft.Text('Páginas'),
                        items=[
                            ft.PopupMenuItem(
                                icon=ft.icons.POST_ADD,
                                text='Mis Publicaciones',
                                on_click=lambda e: page.go('/my-posts')
                            ),
                            ft.PopupMenuItem(
                                icon=ft.icons.INFO,
                                text='Sobre Mí',
                                on_click=lambda e: page.go('/about-me')
                            ),
                        ]
                    ),
                    _user_actions,
                ]
            ),
            ft.Container(width=30),

        ]
    )

    return _app_bar
