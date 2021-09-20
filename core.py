from numpy.lib.utils import source
import cleandata
import schedule_maker
import visuallize_schedule
from kivymd.app import MDApp
from kivy.lang import Builder
import os
import cv2
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.swiper import  MDSwiperItem
from kivy.uix.image import Image
import os
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.utils.fitimage import FitImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.imagelist import SmartTileWithLabel

kv="""
        
MDScreen:
    BoxLayout:
        orientation:'vertical'
        MDToolbar:
            id: toolbar
            title: "Amir Hossein Mansouri"
            elevation: 10
            pos_hint: {"top": 1}
            size_hint_y: 0.05

        MDSwiper:
            id: place
            size_hint_y: 0.8
            #height: root.height - toolbar.height - dp(40)-grid.height
            #y: root.height - self.height - toolbar.height - dp(20)-grid.height

        MDGridLayout:
            size_hint_y: 0.15
            id: grid
            rows:2
            MDTextField:
                id: input_excel_path
                hint_text: 'path of excel'
                icon_right: 'path'
                required: True
                helper_text_mode: 'on_error'
                helper_text:'incorrect file :('
                font_size: 10
            MDTextField:
                id: output_folder_path
                hint_text: 'output folder path'
                icon_right: 'path'
                required: True
                helper_text_mode: 'on_error'
                helper_text:'incorrect path :('
                font_size: 10
            MDTextField:
                id: my_courses
                hint_text: 'please enter your courses id by a space'
                icon_right: 'path'
                required: True
                helper_text_mode: 'on_error'
                #helper_text:'incorrect path :('
                font_size: 10
            MDRoundFlatButton:
                text: 'build'
                on_release: app.run_background()
            #MDRoundFlatButton:
            #    text: 'show'
            #    on_release: app.click()


"""


from kivymd.uix.gridlayout import MDGridLayout
MDGridLayout.on_touch_move
class Choose_Course_App(MDApp):

    def build(self):
        return Builder.load_string(kv)

    def click(self):
        root, folder, files = list(os.walk(self.root.ids.output_folder_path.text.replace("\\", "/")+'/schedules'))[0]#self.root.ids.output_folder_path.text+'/schedules'):
        n = len(files)
        for i in range(n):
            label = str(files[i])
            path = root+'/'+label
            swp = MDSwiperItem()
            swp.add_widget(Image(source = path))
            self.root.ids.place.add_widget(swp)

    def run_background(self):
        df = cleandata.get_input_excel_path(self.root.ids.input_excel_path.text.replace("\\", "/"))
        lst = schedule_maker.get_my_courses(self.root.ids.my_courses.text.split(' '), df)
        visuallize_schedule.get_output_folder_path(self.root.ids.output_folder_path.text.replace("\\", "/"), df,lst)
        self.click()

if __name__ == '__main__':
    Choose_Course_App().run()