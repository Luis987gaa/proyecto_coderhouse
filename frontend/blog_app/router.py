import flet as ft
from .components.appbar import app_bar

# imports views
from .views.register_view import register_view
from .views.login_view import login_view
from .views.posts_views import posts_view
from .views.my_posts_view import my_posts_view
from .views.about_me import about_me_view
from .views.not_found_view import not_found_view
from .views.post_view import post_view


def user_is_loged(page: ft.Page) -> bool:
    """ Funcion que se encarga de ver si el usuario esta logeado. """
    if page.client_storage.contains_key('user_id') and page.client_storage.contains_key('token'):
        return True
    else:
        return False


def main_router(page: ft.Page):
    page.title = "Blog app"

    def route_change(route):

        page.views.clear()

        troute = ft.TemplateRoute(page.route)

        if troute.match('/'):
            page.views.append(posts_view(page))
        elif troute.match('/login'):
            page.views.append(login_view(page))
        elif troute.match('/register'):
            page.views.append(register_view(page))
        elif troute.match('/about-me'):
            page.views.append(about_me_view(page))
        elif troute.match('/my-posts'):
            if user_is_loged(page):
                page.views.append(my_posts_view(page))
            else:
                page.route = '/login'
        elif troute.match('/post/:id'):
            post_id: str = troute.id
            if post_id.isnumeric():
                page.views.append(post_view(page, troute.id, user_is_loged(page)))
            else:
                page.route = '/not-found'

        else:
            page.views.append(not_found_view(page))

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_connect = route_change
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
