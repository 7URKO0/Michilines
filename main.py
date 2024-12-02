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

    def show_file_chooser(self):
        try:
            self.ensure_directory()
            # Filtrar solo archivos de imagen
            filters = [("Image files", "*.jpg", "*.jpeg", "*.png", "*.gif")]
            filechooser.open_file(
                on_selection=self.selected_image,
                filters=filters,
                multiple=False
            )
        except Exception as e:
            print(f"Error al abrir selector de archivos: {e}")

    def selected_image(self, selection):
        try:
            if selection and os.path.exists(selection[0]):
                # Crear una copia de la imagen en assets/images
                filename = os.path.basename(selection[0])
                destination = f'assets/images/{filename}'
                shutil.copy2(selection[0], destination)
                
                # Actualizar preview
                self.ids.preview_image.source = destination
                self.selected_image_path = destination
            else:
                print("No se seleccionó ningún archivo o el archivo no existe.")
        except Exception as e:
            print(f"Error al seleccionar imagen: {e}")

    def submit_form(self):
        # Get form data
        imagen = getattr(self, 'selected_image_path', 'assets/images/pet_placeholder.jpg')
        self.add_pet_to_gallery(
            self.ids.nombre_mascota.text,
            self.ids.edad_mascota.text,
            self.ids.tipo_mascota.text,
            self.ids.ubicacion.text,
            self.ids.estado.text,
            self.ids.descripcion.text,
            imagen
        )
        
        # Clear form and return to main screen
        self.goto_main()

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
