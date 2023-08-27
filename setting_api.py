import flet as ft
import os
import dotenv 

try:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    PINECONE_INDEX_NAME = os.environ.get('PINECONE_INDEX_NAME')
    PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENVIRONMENT')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
except:
    pass

class set_api(ft.UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page=page
        self.openapi = ft.TextField(
            label="OPENAI_API_KEY", password=True, can_reveal_password=True,on_submit=self.env_set,
        )
        self.pnindex = ft.TextField(
            label="PINECONE_INDEX_NAME", on_submit=self.env_set,
        )
        self.pnenv = ft.TextField(
            label="PINECONE_ENVIRONMENT", on_submit=self.env_set, value="gcp-starter"
        )
        self.pnapi = ft.TextField(
            label="PINECONE_API_KEY", password=True, can_reveal_password=True,on_submit=self.env_set,
        )
        self.allbtn=ft.FilledButton("All Submit",on_click=self.all_submit)

        
    def env_set(self,e):
        submitlist=[]
        submitlist.append(self.env_submit(e.control).strip())
        self.snackbar_print(submitlist)

    def all_submit(self,e):
        submitlist=[]
        submitlist.append(self.env_submit(self.openapi).strip())
        submitlist.append(self.env_submit(self.pnindex).strip())
        submitlist.append(self.env_submit(self.pnenv).strip())
        submitlist.append(self.env_submit(self.pnapi).strip())
        self.snackbar_print(submitlist)
        
        # submitlist = [item for item in submitlist if item is not None]

        # if len(submitlist)==0:
        #     e.page.show_snack_bar(ft.SnackBar(ft.Text("Nothing"), open=True))
        # else:
        #     submittext=", ".join(submitlist)
        #     e.page.show_snack_bar(ft.SnackBar(ft.Text(submittext+" is Set"), open=True))

    def snackbar_print(self,submitlist:[]):
        submitlist = [item for item in submitlist if item is not None]
        
        if len(submitlist)==0:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Nothing"), open=True))
        else:
            submittext=", ".join(submitlist)
            self.page.show_snack_bar(ft.SnackBar(ft.Text(submittext+" is Set"), open=True))
    
    def env_submit(self,textenv:ft.TextField):
        try:
            if textenv.value:
                self.page.session.set(textenv.label,textenv.value)
                print (textenv.label)
                print (textenv.value)
                return textenv.label
        except:
            return
        
    def build_page(self):
        self.page.controls.clear()
        return ft.Column([ft.Container(
            content=ft.Column(
            [
                ft.Text("OPEN AI API", style=ft.TextThemeStyle.DISPLAY_SMALL),
                self.openapi,
                ft.Text("PINECONE API", style=ft.TextThemeStyle.DISPLAY_SMALL),
                self.pnindex,
                self.pnenv,
                self.pnapi,
                self.allbtn
            ],
        ),
        padding=50
        )])


if __name__ == "__main__":
    def main(page: ft.Page):
        AIchat=set_api(page)
        page.add(AIchat.build_page())
        page.scroll="AUTO"
        page.on_resize=page.update()
        page.update()
    
    ft.app(main)