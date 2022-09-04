from PIL import ImageFont, Image, ImageDraw, ImageColor
from random import seed, choice
from os import makedirs
from shutil import rmtree
from os.path import isdir

from arabic_reshaper import reshape
from bidi.algorithm import get_display
from tqdm.auto import tqdm

from Custom_Data import custom_data

class visualize:
    text_color = '#4c5760'
    border_color = '#4c5760'
    box_colors = ['#003d5b', '#30638e', '#00798c', '#d1495b', '#edae49']
    box_text_color = '#ffffff'
    background_color = '#e7ecef'

    def __init__(self, name, data, process_results):
        bar = tqdm(total=100, desc='Visualize')
        self.name = name
        self.background_color_rgb = ImageColor.getcolor(self.background_color, "RGB")

        path = f'./results_{name}'
        if isdir(path):
            rmtree(path)

        self.pps = path+'/possible_schedules'
        self.pedc = path+'/classes_of_each_day'
        
        makedirs(self.pps)
        makedirs(self.pedc)

        self.data = data
        self.process_results = process_results

        self.temp_image = Image.new('RGB', (1500, 700))
        self.temp_draw = ImageDraw.Draw(self.temp_image)

        bar.update(2)
        self.__create_schedules()
        bar.update(49)
        self.__create_chart_of_classes_of_each_day()
        bar.update(49)

    def __get_font(self, font_size=17):
        return ImageFont.truetype('./data/Vazir.ttf', font_size)

    def __get_text_size(self, text, font):
        reshaped_text = reshape(text)
        bidi_text = get_display(reshaped_text)
        return self.temp_draw.textsize(bidi_text, font)

    def __box_color(self, x):
        x = int(x.replace('_', ''))
        seed(x)
        return choice(self.box_colors)

    def __put_persian_text(self, text , pos, color, font = None):

        if font == None:
            font = self.__get_font(17)

        reshaped_text = reshape(text)
        bidi_text = get_display(reshaped_text)
        self.draw.text(pos, bidi_text, color, font = font) 

    def __put_course(self, start_time, end_time, course_name, professor_name, course_id, day_index = None):

        start_time = [int(i) for i in start_time.split(':')]
        end_time = [int(i) for i in end_time.split(':')]

        
        w = int(123*(end_time[0]-start_time[0] + (end_time[1]-start_time[1])/60))
        h = 70
        
        if start_time[1] == 30:
            x = 145+123*(start_time[0]-8)+60
        else:
            x = 145+123*(start_time[0]-8)

        def color_check(day_index):
            y = 60+70*day_index+h/2
            for i in range(x+10, x+w-10, 50):
                if self.image.getpixel((i, y)) != self.background_color_rgb:
                    return False
            return True

        if day_index == None:
            for day_index in range(10):
                if color_check(day_index):
                    break

        y = 60+70*day_index

        self.draw.rectangle(
            [(x,y), (x+w,y+h)], 
            fill = self.__box_color(course_id), 
            width = 2
        )
        for i, text in enumerate([course_name, professor_name, course_id]):
            text = text.strip()

            font_size = 17
            t_w, t_h = self.__get_text_size(text, self.__get_font(font_size))
            
            while w-t_w < -5:
                font_size -= 1
                font = self.__get_font(font_size)
                t_w, t_h = self.__get_text_size(text, font)

            font = self.__get_font(font_size)
            
            self.__put_persian_text(
                text,
                (round(x+w/2-t_w/2),round(y+h*i/3)), 
                self.box_text_color,
                font
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
                    font = self.__get_font(28)
                ) 
                self.draw.text(
                    (50+123*j,25), 
                    f"{j+8}:00", 
                    self.text_color, 
                    font = self.__get_font(28)
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
                    professor_name = professor_name.replace('<BR>', ' ')

                    for time in times:

                        if time.type > 1:
                            continue

                        self.__put_course(
                            time.start_time, 
                            time.end_time,  
                            course_name, 
                            professor_name, 
                            course_id,
                            time.day
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
                        self.__get_font(28)
                    )
                    self.draw.line(
                        [(0,130+70*j), (1500,130+70*j)], 
                        fill = self.border_color, 
                        width = 3
                    )

                self.__put_persian_text(
                    'https://github.com/A-H-Mansoury/schedule_maker',
                    (1020, 650), 
                    self.text_color, 
                    self.__get_font(18)
                )

                self.image.save(f"{self.pps}/schedule_{i}.jpg")
    


    def __create_chart_of_classes_of_each_day(self):
    
        for i in range(len(custom_data.WEEKDAYS)):
            setattr(self, 'image_%d'%i , Image.new('RGB', (1500, 700), self.background_color))
            image_i = getattr(self, 'image_%d'%i)
            setattr(self, 'draw_%d'%i , ImageDraw.Draw(image_i))
            
        lst = self.data[['container','نام درس', 'نام استاد', 'شماره و گروه درس']].values.tolist()
        for times, course_name, professor_name, course_id in lst:
            professor_name = professor_name.replace('<BR>', ' ')
            for time in times:

                if time.type > 1:
                    continue
                
                self.draw = getattr(self, 'draw_%d' % time.day)
                self.image = getattr(self, 'image_%d' % time.day)
                
                self.__put_course(
                    time.start_time, 
                    time.end_time, 
                    course_name, 
                    professor_name, 
                    course_id
                )

        for i in range(len(custom_data.WEEKDAYS)):    
            self.image = getattr(self, 'image_%d'%i)
            self.draw = getattr(self, 'draw_%d'%i)

            self.__put_persian_text(
                custom_data.WEEKDAYS[i],
                (20,12), 
                self.text_color, 
                self.__get_font(28)
            )

            for j in range(1,11):
                self.draw.text(
                    (50+123*j,0), 
                    f"{j+7}:00", 
                    self.text_color, 
                    font = self.__get_font(28)
                ) 
                self.draw.text(
                    (50+123*j,25), 
                    f"{j+8}:00", 
                    self.text_color, 
                    font = self.__get_font(28)
                ) 
                self.draw.line(
                    [(145+123*j,0), (145+123*j,60)], 
                    fill = self.border_color, 
                    width = 2
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

            for j in range(10):
                self.__put_persian_text(
                    '%s %d' % ('کلاس', j),
                    (20,75+70*j), 
                    self.text_color, 
                    self.__get_font(28)
                )
                self.draw.line(
                    [(0,130+70*j), (1500,130+70*j)], 
                    fill = self.border_color, 
                    width = 3
                )

            self.__put_persian_text(
                'https://github.com/A-H-Mansoury/schedule_maker',
                (1020, 650), 
                self.text_color, 
                self.__get_font(18)
            )
            self.image.save(f"{self.pedc}/{custom_data.WEEKDAYS[i]}.jpg")
