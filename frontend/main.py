import flet as ft
from app.router import app_router


def main(page: ft.Page):
    """ Configuraciones principales del projecto """
    page.theme_mode = 'light'
    page.bgcolor = "#4ebbd5"
    page.scroll = True
    page.fonts = {
        "Milky": "fonts/MilkyHoney.ttf",
        "Rubik": "fonts/RubikMarkerHatch-Regular.ttf",
        "Louis": "fonts/LouisGeorgeCafe.ttf",
        "Vintage": "fonts/VintageKing.ttf"
    }
    #page.show_semantics_debugger = True
    page.theme = ft.Theme(
        font_family="Louis",
    )
    app_router(page)


ft.app(target=main, assets_dir="app/assets", view=ft.WEB_BROWSER)
