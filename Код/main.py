import customtkinter

from AI import *
from time import *
from tkinter import filedialog  # Импортируем диалоговое окно
from PIL import Image  # Для отображения выбранного фото (необязательно)

class App(customtkinter.CTk):
    def back(self,screen_w,screen_h):
        self.image.configure(dark_image=Image.open(resource_path('logo.png')), size=(int(0.353 * screen_w), int(0.551 * screen_h)))
        self.plus_info.configure(state='normal', text='Выберите файл')
        self.label_path.configure(text='')
        self.res.configure(text='')
        self.no.destroy()
        self.yes.destroy()

    def analyse(self,screen_w,screen_h,file_path):
        self.no.destroy()
        self.yes.destroy()
        sleep(3)
        results = Naming(file_path)
        if results["acute_mi"] > 0:
            r = f"Признаков инфаркта миокарда: {results['acute_mi']}.\nИтог: Требуется срочная госпитализация!"
        elif results["anomaly"] > 0:
            r = f"Аномальных сокращений: {results['anomaly']}.\nИтог: Требуется консультация кардиолога."
        elif results['normal'] > 0:
            r = "Итог: Ритм сердца в норме."
        else:
            r = "Фото не подходит для анализа."
        self.res.configure(text=f'{r}',font=('Segoe UI',20))
        t = file_path.split('/')[-1].split('.')[0]
        self.image.configure(dark_image=Image.open(f'runs/detect/ECG_Results/{t}.jpg'), size=(int(0.49*screen_w), int(0.6*screen_h)),pady=(0, 0))
        self.plus_info.configure(state='normal',text="Выберите файл")

    def select_file(self,screen_w,screen_h):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение ЭКГ",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            print(f"Выбран файл: {file_path}")

            self.label_path.configure(text=f"Файл: {file_path.split('/')[-1]}",font=('Segoe UI',15))

            self.plus_info.configure(state='disabled', text='Обработка...')

            self.image.configure(dark_image=Image.open(f'{file_path}'), size=(int(0.49*screen_w), int(0.6*screen_h)),pady=(0, 0))
            self.res.configure(text='Анализировать это изображение?',font=('Segoe UI',20))

            self.yes = customtkinter.CTkButton(self, text="✓", width=30, height=30, command= lambda : self.analyse(screen_w,screen_h,file_path))
            self.yes.grid(row=4, column=0, pady=(0, int(90/1080*screen_h)), padx=(int(1080/1920*screen_w), 5))

            self.no = customtkinter.CTkButton(self, text="✗", width=30, height=30, command= lambda: self.back(screen_w,screen_h))
            self.no.grid(row=4, column=0, pady=(int(90/1080*screen_h), 0), padx=(int(1080/1920*screen_w), 5))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Эхо сердца")
        self.after(0, lambda: app.state('zoomed'))

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        self.hello = customtkinter.CTkLabel(self, width=screen_w, height=70, text="ПРОГРАММА ЭХО СЕРДЦА", fg_color="transparent", justify='center', anchor = 'center')
        self.hello.grid(row=0, column=0, pady= (int(45/1080*screen_h),0))
        self.hello.configure(font=('Montserrat', 38,'bold'))

        self.change_lab = customtkinter.CTkLabel(self, width=800, height=40, text="Импортируйте скан ЭКГ", fg_color="transparent", justify='center', anchor = 'center',font=('Segoe UI',22))
        self.change_lab.grid(row=1, column=0, pady=(int(35/1080*screen_h), 0))

        self.plus_info = customtkinter.CTkButton(self, width=180 ,height=44, text="Выберите файл", command= lambda: self.select_file(screen_w,screen_h))
        self.plus_info.grid(row=2, column=0, pady=(int(6/1080*screen_h), 0))

        self.label_path = customtkinter.CTkLabel(self, text="", height=30)
        self.label_path.grid(row=3, column=0, pady=(int(20/1080*screen_h), int(10/1080*screen_h)))

        self.image = customtkinter.CTkImage(dark_image=Image.open(resource_path('logo.png')), size=(int(0.353 * screen_w), int(0.551 * screen_h)))
        self.image_label = customtkinter.CTkLabel(self, image=self.image, text="", anchor='center', justify='center')
        self.image_label.grid(row=4, column=0, pady=(0, 0))

        self.res = customtkinter.CTkLabel(self, width=800, height=43, text='',
                                          fg_color="transparent", justify='center', anchor='center')
        self.res.grid(row=5, column=0, pady=(int(5/1080*screen_h), int(20/1080*screen_h)))

app = App()
app.iconbitmap(resource_path('logo.ico'))
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure((0, 1, 2, 3), weight=1)
app.mainloop()