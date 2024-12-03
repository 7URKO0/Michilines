import kivy
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from utils.colors import new_rgb_color
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from plyer import filechooser
import os
import shutil


kivy.require('2.3.0')


# Add custom fonts
LabelBase.register(
    name='Montserrat', 
    fn_regular='assets/fonts/Montserrat-Bold.ttf'
)


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def change_color(self):
        self.main_title.color = new_rgb_color()

    def goto_form(self):
        self.ids.screen_manager.current = 'form'

    def goto_main(self):
        self.ids.screen_manager.current = 'main'

    def goto_gallery(self):
        self.ids.screen_manager.current = 'gallery'

    def ensure_directory(self):
        if not os.path.exists('assets/images'):
            os.makedirs('assets/images')

    def add_pet_to_gallery(self, nombre, edad, tipo, ubicacion, estado, descripcion, imagen='assets/images/pet_placeholder.jpg'):
        pet_card = BoxLayout(orientation='vertical', size_hint_y=None, height=400, padding=10, spacing=5)
        pet_card.canvas.before.add(Color(0.9, 0.9, 0.9, 1))
        pet_card.canvas.before.add(Rectangle(pos=pet_card.pos, size=pet_card.size))
        
        # Add image
        image = Image(source=imagen, size_hint_y=0.6)
        pet_card.add_widget(image)
        
        # Add pet information
        info_labels = [
            f'Nombre: {nombre}',
            f'Edad: {edad}',
            f'Tipo: {tipo}',
            f'Ubicación: {ubicacion}',
            f'Estado: {estado}',
            f'Descripción: {descripcion}'
        ]
        
        for text in info_labels:
            label = Label(
                text=text,
                size_hint_y=None,
                height=30,
                text_size=(pet_card.width, None),
                halign='left'
            )
            pet_card.add_widget(label)
        
        # Add to gallery grid
        self.ids.gallery_grid.add_widget(pet_card)


class HelloWorld(App):

    # .kv files path
    kv_directory = "templates"

    def build(self):
        # return Label(text="Hello World!")
        return MyRoot()

    
if __name__ == "__main__":
    app = HelloWorld()
    app.run()
