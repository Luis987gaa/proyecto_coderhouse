import flet as ft
import httpx
import json
from ..components.appbar import app_bar
from typing import Dict


class PostView(ft.UserControl):

    _file_picker = ft.FilePicker()

    _prog_bars: Dict[str, ft.ProgressRing] = {}
    _files = ft.Ref[ft.Column]()

    _image = ft.Image(height=200)

    _btn_pick_img = ft.TextButton(
        text='Abrir imagen...',
        icon=ft.icons.FOLDER_OPEN,
    )

    _btn_upload_img = ft.TextButton(
        text='Subir Imagen',
        icon=ft.icons.UPLOAD,
        disabled=True
    )

    _btn_img_container = ft.Column(
        visible=False
    )

    _btn_save = ft.TextButton(
        icon=ft.icons.SAVE,
        text='Guardar',
        visible=False,
    )

    _btn_edit = ft.TextButton(
        icon=ft.icons.EDIT_NOTIFICATIONS,
        text='Editar',
    )

    _btn_delete = ft.TextButton(
        icon=ft.icons.DELETE_SWEEP,
        text='Eliminar')

    _main_container = ft.Container()
    _main_card = ft.Card()
    _post_container = ft.Container(
        padding=30,
    )

    _text_inpup_titulo = ft.TextField(visible=False)
    _text_inpup_subtitulo = ft.TextField(visible=False)
    _text_inpup_contenido = ft.TextField(visible=False, multiline=True)

    _text_titulo = ft.Text(style=ft.TextThemeStyle.TITLE_SMALL, weight=ft.FontWeight.BOLD)
    _text_sub_titulo = ft.Text(style=ft.TextThemeStyle.BODY_LARGE)
    _text_contenido = ft.Text(style=ft.TextThemeStyle.BODY_SMALL)
    _url_image = ft.Text()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_data(self):
        response = httpx.get(f'http://127.0.0.1:8000/api/post/{self.data["id"]}').content.decode('latin-1')
        return json.loads(response)

    def edit_actived(self, e):

        self._text_inpup_titulo.value = self._text_titulo.value
        self._text_inpup_subtitulo.value = self._text_sub_titulo.value
        self._text_inpup_contenido.value = self._text_contenido.value

        self._text_inpup_titulo.visible = True
        self._text_inpup_subtitulo.visible = True
        self._text_inpup_contenido.visible = True
        self._btn_save.visible = True
        self._btn_img_container.visible = True

        self._text_titulo.visible = False
        self._text_sub_titulo.visible = False
        self._text_contenido.visible = False
        self._btn_edit.visible = False

        self.update()

    def save_actived(self, e):

        self._btn_save.disabled = True
        self._btn_save.update()

        data = {
            "titulo": self._text_inpup_titulo.value,
            "sub_titulo": self._text_inpup_subtitulo.value,
            "contenido": self._text_inpup_contenido.value,
            "autor": self.data['user_id'],
            "image_post": self.data['image_post']
        }

        headers = httpx.Headers(
            {"Authorization": f"Token {self.data['token']}",
             "Content-Type": "application/json"})

        response = httpx.put(f'http://127.0.0.1:8000/api/post/update/{self.data["id"]}', json=data, headers=headers)

        print(response.status_code)

        data_str = response.content.decode('latin')

        print(data_str)

        data_dict = json.loads(data_str)

        self._btn_save.disabled = False

        self._text_inpup_titulo.visible = False
        self._text_inpup_subtitulo.visible = False
        self._text_inpup_contenido.visible = False
        self._btn_save.visible = False
        self._btn_img_container.visible = False

        self._text_titulo.value = data_dict['titulo']
        self._text_sub_titulo.value = data_dict['sub_titulo']
        self._text_contenido.value = data_dict['contenido']

        self._text_titulo.visible = True
        self._text_sub_titulo.visible = True
        self._text_contenido.visible = True
        self._btn_edit.visible = True

        self._image.src = data_dict['image_post']

        self.update()

    def input_titulo_changed(self, e):
        self._text_inpup_titulo.value = e.control.value
        self._text_inpup_titulo.update()

    def input_subtitulo_changed(self, e):
        self._text_inpup_subtitulo.value = e.control.value
        self._text_inpup_subtitulo.update()

    def input_contenido_changed(self, e):
        self._text_inpup_contenido.value = e.control.value
        self._text_inpup_contenido.update()

    def delete_activated(self, e):

        headers = httpx.Headers(
            {"Authorization": f"Token {self.data['token']}",
             "Content-Type": "application/json"})
        response = httpx.delete(f'http://127.0.0.1:8000/api/post/delete/{self.data["id"]}', headers=headers)

        if response.status_code == 204:
            self.page.go('/my-posts')

        elif response.status_code == 404:
            self.page.go('/not-post-found')

        elif response.status_code == 401:
            self.page.go('/not-authorizaded')

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        self._btn_upload_img.disabled = True if e.files is None else False
        self._prog_bars.clear()

        self._files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ft.ProgressRing(value=0, width=20, height=20)
                self._prog_bars[f.name] = prog
                self._files.current.controls.append(ft.Row([prog, ft.Text(f.name)]))
            self.update()

    def on_upload_progress(self, e: ft.FilePickerUploadEvent):
        self._prog_bars[e.file_name].value = e.progress
        self._prog_bars[e.file_name].update()

    def upload_file(self, e):
        uf = []
        print(self._file_picker.result)
        print(self._file_picker.result.files)
        if self._file_picker.result is not None and self._file_picker.result.files is not None:

            for f in self._file_picker.result.files:
                uf.append(
                    ft.FilePickerUploadFile(
                        name=f.name,
                        upload_url=self.page.get_upload_url(
                            f"user-{self.data['user_id']}/img-post{self.data['id']}/{f.name}",
                            50),
                    )
                )
                self.data['image_post'] = f"user-{self.data['user_id']}/img-post{self.data['id']}/{f.name}"
                self.update()
            self._file_picker.upload(uf)

    def did_mount(self):

        dict_data = self.get_data()

        self._text_titulo.value = dict_data['titulo']
        self._text_sub_titulo.value = dict_data['sub_titulo']
        self._text_contenido.value = dict_data['contenido']
        self.data['image_post'] = dict_data['image_post']

        print(dict_data)
        print('¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿')
        print(self.data)

        if self.data['user_loged']:
            if self.data['user_id'] == dict_data['autor_id']:

                self._file_picker.on_result = self.file_picker_result
                self._file_picker.on_upload = self.on_upload_progress

                self.page.overlay.append(self._file_picker)
                self.page.update()

                self._image.src = self.data['image_post']

                self._btn_pick_img.on_click = lambda e: self._file_picker.pick_files(allow_multiple=False)
                self._btn_upload_img.on_click = lambda e: self.upload_file(e)

                self._btn_img_container.controls = [
                                ft.Row(controls=[
                                    self._btn_pick_img,
                                    ft.Column(ref=self._files),
                                    self._btn_upload_img,
                                ])
                            ]

                self._post_container.content = ft.ResponsiveRow(
                    controls=[
                        ft.Column(
                            controls=[
                                self._text_titulo,
                                self._text_inpup_titulo]),
                        ft.Column(
                            controls=[
                                self._text_sub_titulo,
                                self._text_inpup_subtitulo]),
                        ft.Column(
                            controls=[
                                self._text_contenido,
                                self._text_inpup_contenido]),
                        ft.Column(height=20),
                        ft.Column(
                            controls=[
                                self._image
                            ]
                        ),
                        ft.Column(height=20),
                        ft.Column(controls=[
                            ft.Text(value=f"Publicado por - {dict_data['autor']}",
                                    style=ft.TextThemeStyle.BODY_SMALL), ]),
                        self._btn_img_container,
                        ft.Column(controls=[
                            ft.Row(
                                controls=[
                                    self._btn_save,
                                    self._btn_edit,
                                    self._btn_delete,
                                ]
                            )
                        ])
                    ]

                )
            else:
                self._post_container.content = ft.ResponsiveRow(
                    controls=[
                        ft.Column(controls=[ft.Text(
                            value=dict_data['titulo'],
                            style=ft.TextThemeStyle.TITLE_LARGE,
                            weight=ft.FontWeight.BOLD,
                        ), ]),
                        ft.Column(
                            controls=[ft.Text(value=dict_data['sub_titulo'], style=ft.TextThemeStyle.TITLE_SMALL), ]),
                        ft.Column(
                            controls=[ft.Text(value=dict_data['contenido'], style=ft.TextThemeStyle.BODY_LARGE), ]),
                        ft.Column(
                            controls=[
                                ft.Image(src=self.data['image_post'], height=200)
                            ]
                        ),
                        ft.Column(controls=[
                            ft.Text(value=f"Publicado por - {dict_data['autor']}",
                                    style=ft.TextThemeStyle.BODY_SMALL), ]),
                    ]

                )
        else:
            self._post_container.content = ft.ResponsiveRow(
                controls=[
                    ft.Column(controls=[ft.Text(
                        value=dict_data['titulo'],
                        style=ft.TextThemeStyle.TITLE_LARGE,
                        weight=ft.FontWeight.BOLD,
                    ), ]),
                    ft.Column(controls=[ft.Text(value=dict_data['sub_titulo'], style=ft.TextThemeStyle.TITLE_SMALL), ]),
                    ft.Column(controls=[ft.Text(value=dict_data['contenido'], style=ft.TextThemeStyle.BODY_LARGE), ]),
                    ft.Column(
                        controls=[
                            ft.Image(src=self.data['image_post'], height=200)
                        ]
                    ),
                    ft.Column(controls=[
                        ft.Text(value=f"Publicado por - {dict_data['autor']}",
                                style=ft.TextThemeStyle.BODY_SMALL), ]),
                ]

            )

        self._text_inpup_titulo.on_change = lambda e: self.input_titulo_changed(e)
        self._text_inpup_subtitulo.on_change = lambda e: self.input_subtitulo_changed(e)
        self._text_inpup_contenido.on_change = lambda e: self.input_contenido_changed(e)

        self._btn_edit.on_click = lambda e: self.edit_actived(e)
        self._btn_save.on_click = lambda e: self.save_actived(e)
        self._btn_delete.on_click = lambda e: self.delete_activated(e)

        self._main_card.content = self._post_container
        self._main_container.content = self._main_card
        self._main_container.update()

    def build(self):
        self._main_container.content = ft.ProgressRing(width=50, height=50, stroke_width=5)
        return self._main_container


def post_view(page: ft.Page, post_id, user_loged) -> ft.View:
    if user_loged:
        data = {
            'id': post_id,
            'user_loged': user_loged,
            'token': page.client_storage.get('token'),
            'user_id': page.client_storage.get('user_id'),
        }
    else:
        data = {
            'id': post_id,
            'user_loged': user_loged
        }

    _post_view = PostView(data=data)

    _view = ft.View(
        horizontal_alignment=ft.CrossAxisAlignment('center'),
        vertical_alignment=ft.MainAxisAlignment('center'),
        appbar=app_bar(page),
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Column(col={'sm': 12, 'md': 2}, controls=[]),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        col={'sm': 12, 'md': 8},
                        controls=[_post_view]),
                    ft.Column(col={'sm': 12, 'md': 2}, controls=[]),
                ]
            ),
        ]
    )

    return _view
