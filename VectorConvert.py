import flet as ft
import os
from module_langchain.embedding_vector2json import embeddingfiles2json

class VectorConvert(ft.UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page=page
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.selected_files = ft.Text()
        self.picker=ft.ElevatedButton(
            "Pick files",
            icon=ft.icons.ATTACH_FILE,
            on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=True, file_type="custom",allowed_extensions= ['pdf','docx']),
            )
        self.jsonfile=ft.FilledButton(
            "Convert",
            icon=ft.icons.DRIVE_FILE_MOVE_OUTLINED,
            on_click=self.convert2json,
            visible=False
            )
        self.filetext=ft.Text(style=ft.TextThemeStyle.LABEL_LARGE)
        self.progress=ft.Column([
            self.filetext,
            ft.ProgressBar(),
            ],
            visible=False

        )
        self.donelist=ft.Text(style=ft.TextThemeStyle.LABEL_MEDIUM)
        self.donetext=ft.Column([
            ft.Text("DONE",style=ft.TextThemeStyle.LABEL_MEDIUM),
            self.donelist,
            ],
            visible=False
        )
        self.files=[]


        
    def pick_files_result(self,e: ft.FilePickerResultEvent):
        self.jsonfile.visible=False
        self.jsonfile.update()
        self.donetext.visible=False
        self.donetext.update()
        files=[]
        paths=[]
        if e.files:
            for f in e.files:
                files.append(f.name)
                paths.append(f.path)
            self.selected_files.value ="\n ".join(files)
            self.jsonfile.visible=True
            self.jsonfile.update()
        else:
            self.selected_files.value ="Cancelled!"
        self.files=paths
        self.selected_files.update()

    def convert2json(self,e):
        jsonfiles=[]
        self.donetext.visible=False
        self.donetext.update()
        if len(self.files)==0:
            return
        if not self.open_api:
            return
        
        self.progress.visible=True
        self.progress.update()
        for filename in self.files:
            self.filetext.value="Convert 2 Json - " + os.path.basename(filename)
            self.progress.update()
            jsonpath=embeddingfiles2json([filename],self.open_api)
            self.page.show_snack_bar(ft.SnackBar(ft.Text(f"{filename} is done"), open=True))
            jsonfiles.append(os.path.basename(jsonpath))
            if len(jsonfiles)>0:
                donelist=" \n".join(jsonfiles)
                self.donelist.value=donelist
                self.donetext.visible=True
                self.donetext.update()
        
        self.progress.visible=False
        self.progress.update()

    def build_page(self):
        self.page.controls.clear()
        self.open_api=self.page.session.get("OPENAI_API_KEY")
        return ft.Column(
            [
                self.pick_files_dialog,
                self.picker,
                self.selected_files,
                self.jsonfile,
                self.progress,
                self.donetext,
            ]
        )


if __name__ == "__main__":
    def main(page: ft.Page):
        page.session.set("OPENAI_API_KEY","JH")
        AIchat=VectorConvert(page)
        page.add(AIchat.build_page())
        page.scroll="AUTO"
        page.on_resize=page.update()
        page.update()
    
    ft.app(main)