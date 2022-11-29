from flet import Page, TemplateRoute
import json

# pages imports
from app.views.login import LoginPage
from app.views.register import RegisterPage
from app.views.no_found_page import NotFoundPage
from app.views.home import HomePage
from app.views.myposts import MyPostsPage
from app.views.personal_info import AboutMePage


def app_router(page: Page):

    def get_user_data():
        if page.client_storage.contains_key('credentials'):
            user_srt_data = page.client_storage.get('credentials')
            user_dict_data = json.loads(user_srt_data)
            return True, user_dict_data
        else:
            return False, {}

    def route_change(route):
        page.controls.clear()

        user_log, user_data = get_user_data()

        troute = TemplateRoute(page.route)

        if troute.match('/'):
            get_user_data()
            page.add(HomePage(page))

        elif troute.match('/login'):
            page.add(LoginPage(page))

        elif troute.match('/register'):
            page.add(RegisterPage(page))

        elif troute.match('/mis-posts'):
            user_id = page.client_storage.get('user_id')
            page.add(HomePage(page, user_log, user_data))

        elif troute.match('/posts/:id'):
            page.add(HomePage(page, troute.id))

        elif troute.match('/about-me'):
            page.add(AboutMePage(page))

        elif troute.match('/logout'):
            page.client_storage.clear()
            page.go('/')
        else:
            page.add(NotFoundPage(page))  # Se renderiza cuando la pagina no existe.
        page.update()

    page.on_route_change = route_change
    page.go(page.route)
