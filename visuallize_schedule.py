import cv2 as cv
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageFont, ImageDraw
import random
import os
import pandas as pd

font1 = ImageFont.truetype('Vazir.ttf', 17, encoding='unic')
font2 = ImageFont.truetype('Vazir.ttf', 28, encoding='unic')

def get_output_folder_path(path, df, lst):
    try:
        os.chdir(path)
        try:
            os.makedirs('schedules')
        except:
            pass
        os.chdir(path+'/schedules')
    except:
        print('this path does not exist, please choose another one')
        exit()
    run(df, lst)


def put_persian_text(img, text ,pos, color = (0,0,0), font = font1):
    if color == (0,0,0):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    draw.text(pos, bidi_text,color, font = font) 
    img = np.asarray(img)
    if color == (0,0,0):
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    return img

def put_text(img, s1,e1,day_index,color, name, prof, id):
    s1 = [int(i) for i in s1.split(':')]
    e1 = [int(i) for i in e1.split(':')]
    y, w, h =60+70*day_index,int(123*(e1[0]-s1[0]+(e1[1]-s1[1])/60)),70
    if s1[1] == 30: #or e1[0] == 30:
        x = 145+123*(s1[0]-8)+63
    else:
        x = 145+123*(s1[0]-8)
    cv.rectangle(img,(x,y), (x+w,y+h), color,-1,cv.LINE_4)
    img = put_persian_text(img, name,(x+w//10,y))
    img = put_persian_text(img, prof,(x+w//10,y+h//3))
    img = put_persian_text(img, id,(x+w//10,y+h//3*2))
    return img

def run(df, lst):
    global  font2
    days =['','شنبه','یکشنبه', 'دوشنبه', 'سه شنبه','چهارشنبه','پنج شنبه','جمعه']
    blank = 255 * np.ones(shape=[700, 1500, 3], dtype=np.uint8)
    cv.line(blank, (0,60), (1500,60), (100,2, 50), 2 , cv.LINE_4)
    cv.line(blank, (145,0), (145,700), (100,2, 50), 2 , cv.LINE_4)

    for i in range(1,8):
        blank = put_persian_text(blank, days[i],(4,5+70*i), (0,0,255), font2)
        cv.line(blank, (0,60+70*i), (1500,60+70*i), (100,2, 50), 2 , cv.LINE_4)

    for i in range(1,11):
        cv.putText(blank, f"{i+7}:00",(50+123*i,28),cv.FONT_HERSHEY_PLAIN, 1.5, (0,0,255), 1,cv.LINE_4)
        cv.putText(blank, f"{i+8}:00",(50+123*i,50),cv.FONT_HERSHEY_PLAIN, 1.5, (0,0,255), 1,cv.LINE_4)
        cv.line(blank, (145+123*i,0), (145+123*i,60), (100,2, 50), 2 , cv.LINE_4)

    all_courses = dict()
    droped_df = df.drop(['id'], axis=1)

    for id, rw in zip(df['id'], droped_df.to_dict('records')):
        all_courses[id] = rw

    for i, line in enumerate(lst):
        img = blank.copy()
        for id in line:
            clr = (random.randint(100, 255),random.randint(100, 255),random.randint(100, 255))
            temp = all_courses[id]
            dys = eval(temp['days'])
            for index in dys:
                img = put_text(img,temp['Start_time'],temp['end_time'], index,clr, temp['course_name'], temp['prof'], id)

        cv.imwrite(f"program{i}.jpg",img)

    cv.waitKey(0)
    cv.destroyAllWindows()