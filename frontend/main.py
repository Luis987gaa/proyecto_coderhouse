import flet
from blog_app.router import main_router


def main(page: flet.Page):

    page.show_semantics_debugger = False

    page.fonts = {
        "Louis": "fonts/LouisGeorgeCafe.ttf",
        "Milky": "fonts/MilkyHoney.ttf",
        "Rubik": "fonts/RubikMarkerHatchRegular.ttf",
        "Vintage": "fonts/VintageKing.ttf"
    }

    page.theme = flet.Theme(
        visual_density=flet.ThemeVisualDensity.COMFORTABLE,
        use_material3=False,
        font_family="Louis",
        color_scheme_seed="#5f09ab",
    )

    page.dark_theme = flet.Theme(
        visual_density=flet.ThemeVisualDensity.COMFORTABLE,
        font_family="Louis",
        use_material3=False,
        color_scheme_seed="#700cc7",
    )

    # Inclusion del router principal
    main_router(page)


flet.app(
    target=main,
    view="web_browser",
    assets_dir="blog_app/assets",
    upload_dir="blog_app/assets"
)
