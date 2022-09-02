from PIL import ImageFont, Image, ImageDraw
from random import seed, choice
from os import mkdir
from shutil import rmtree
from os.path import isdir

from arabic_reshaper import reshape
from bidi.algorithm import get_display

from Custom_Data import custom_data

class visualize:

    font_1 = ImageFont.truetype('./data/Vazir.ttf', 17, encoding='unic')
    font_2 = ImageFont.truetype('./data/Vazir.ttf', 28, encoding='unic')
    font_3 = ImageFont.truetype('./data/Vazir.ttf', 25, encoding='unic')
    text_color = '#4c5760'
    border_color = '#4c5760'
    box_colors = ['#003d5b', '#30638e', '#00798c', '#d1495b', '#edae49']
    box_text_color = '#ffffff'
    background_color = '#e7ecef'

    def __init__(self, name, data, process_results):
        self.name = name
        dir = f'./results_{name}'

        if isdir(dir):
            rmtree(dir)
        
        mkdir(dir)

        self.data = data
        self.process_results = process_results

        self.__create_schedules()

    def __box_color(self, x):
        x = int(x[:-3])
        seed(x)
        return choice(self.box_colors)

    def __put_persian_text(self, text , pos, color, font = None):

        if font == None:
            font = self.font_1

        reshaped_text = reshape(text)
        bidi_text = get_display(reshaped_text)
        self.draw.text(pos, bidi_text, color, font = font) 

    def __put_course(self, start_time, end_time, day_index, course_name, professor_name, course_id):

        start_time = [int(i) for i in start_time.split(':')]
        end_time = [int(i) for i in end_time.split(':')]

        y = 60+70*day_index 
        w = int(123*(end_time[0]-start_time[0] + (end_time[1]-start_time[1])/60))
        h = 70
        
        if start_time[1] == 30:
            x = 145+123*(start_time[0]-8)+60
        else:
            x = 145+123*(start_time[0]-8)
        
        self.draw.rectangle(
            [(x,y), (x+w,y+h)], 
            fill = self.__box_color(course_id), 
            width = 2
        )

        self.__put_persian_text(
            course_name,
            (x+w//10,y), 
            color = self.box_text_color
        )
        self.__put_persian_text(
            professor_name,
            (x+w//10,y+h//3), 
            color = self.box_text_color
        )
        self.__put_persian_text(
            course_id,
            (x+w//10,y+h//3*2), 
            color = self.box_text_color
        )
    
    def __create_schedules(self):

        for i, pr in enumerate(self.process_results):
            self.image = Image.new('RGB', (1500, 700), self.background_color)
            self.draw = ImageDraw.Draw(self.image) 

            for j in range(1,11):
                self.draw.text(
                    (50+123*j,0), 
                    f"{j+7}:00", 
                    self.text_color, 
                    font = self.font_2
                ) 
                self.draw.text(
                    (50+123*j,25), 
                    f"{j+8}:00", 
                    self.text_color, 
                    font = self.font_2
                ) 
                self.draw.line(
                    [(145+123*j,0), (145+123*j,60)], 
                    fill = self.border_color, 
                    width = 2
                )
            
            for course_id in pr:
                data = self.data.loc[
                        self.data['شماره و گروه درس'] == course_id,
                        ['container','نام درس', 'نام استاد']
                    ]
                data = data.values.tolist()

                for times, course_name, professor_name in data: 

                    for time in times:

                        if time.type > 1:
                            continue

                        professor_name = professor_name.replace('<BR>', ' ')

                        self.__put_course(
                            time.start_time, 
                            time.end_time, 
                            time.day, 
                            course_name, 
                            professor_name, 
                            course_id
                        )

                self.draw.line(
                    [(0,60), (1500,60)], 
                    fill = self.border_color, 
                    width = 3
                )

                self.draw.line(
                    [(145,0), (145,700)], 
                    fill = self.border_color, 
                    width = 3
                )

                for j in range(len(custom_data.WEEKDAYS)):
                    self.__put_persian_text(
                        custom_data.WEEKDAYS[j],
                        (20,75+70*j), 
                        self.text_color, 
                        self.font_2
                    )
                    self.draw.line(
                        [(0,130+70*j), (1500,130+70*j)], 
                        fill = self.border_color, 
                        width = 3
                    )

                self.__put_persian_text(
                    'By A-H-Mansoury Summner 2022',
                    (1100, 650), 
                    self.text_color, 
                    self.font_3
                )

                self.image.save(f"./results_{self.name}/schedule_{i}.jpg")
        
