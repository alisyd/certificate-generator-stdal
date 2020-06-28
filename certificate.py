import base64
from flask import session
from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont
import tempfile
import textwrap as tw
import random


class Certificate():
    def __init__(self, name=None,track=None, email=None, user_id=None, mission_id=None):
        self.track = track
        self.name = name
        self.email = email
        self.user_id = user_id
        self.mission_id = mission_id

    def serve_pil_image(self, pil_img):
        img_io = BytesIO()
        pil_img.save(img_io, 'JPG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpg')


    def generate(self):
        name = self.name
        name_list = list(map(lambda string: string.upper(), self.name.split()))
        
        track = self.track
        track_list=list(map(lambda string: string.capitalize(), self.track.split()))
        img = Image.open("templates/template.jpg")
        width, height = img.size
        #self.draw_multiline_text(img,name,font,(225,81,175))

        draw = ImageDraw.Draw(img)
        name_width, name_height = draw.textsize(name)
        print(name,width, name_width, height, name_height)
        print(self.user_id)
        if(len(track_list)==1):
            track_font_size=55
            track_name=track_list[0]
        if((len(track_list)==2)):
            if((len(track_list[0]) + len(track_list[1])) > 15):
                track_font_size=45
        
                track_name = track_list[0] + '\n' + track_list[1]
            else:
                track_font_size=55
                track_name = track_list[0] + '\n' + track_list[1]
            
        elif((len(track_list)==3)):
            if((len(track_list[0]) + len(track_list[1])) < 14):
                track_font_size=50
                track_name = track_list[0] + ' ' + track_list[1] + '\n' + track_list[2]                            
            else:
                track_font_size=50
                track_name = track_list[0] + ' ' + track_list[1] + '\n' + track_list[2]
                
        elif((len(track_list)==4)):
            track_font_size=50
            track_name = track_list[0] + ' ' + track_list[1] + '\n' + track_list[2] + ' ' + track_list[3]
        
        
        
        if((len(name_list)==2)):
            if((len(name_list[0]) + len(name_list[1])) > 10):
                font_size=60
        
                print_name = name_list[0] + '\n' + name_list[1]
            else:
                font_size=70
                print_name = name_list[0] + '\n' + name_list[1]
            
        elif((len(name_list)==3)):
            if((len(name_list[0]) + len(name_list[1])) < 14):
                font_size=60
                print_name = name_list[0] + ' ' + name_list[1] + '\n' + name_list[2]                            
            else:
                font_size=50
                print_name = name_list[0] + ' ' + name_list[1] + '\n' + name_list[2]
                
        elif((len(name_list)==4)):
            font_size=50
            print_name = name_list[0] + ' ' + name_list[1] + '\n' + name_list[2] + ' ' + name_list[3]
        
        track_fill=random.choice([(255,255,0),(255,0,255),(0,255,255), (220,216,12)])
        track_font = ImageFont.truetype('sifonn.otf',track_font_size)            
        draw.text(xy=(352,180), text=track_name, fill=track_fill, font=track_font)   
        

        font_name = ImageFont.truetype('sifonn.otf',font_size)            
        draw.text(xy=(352,363), text=print_name, fill=(225,81,175), font=font_name)   
        img.save( "certificates/"+self.name+"_"+str(self.user_id)+ ".jpg")

