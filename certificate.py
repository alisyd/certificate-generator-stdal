import base64
from flask import session
from io import BytesIO
import os
from PIL import Image, ImageDraw, ImageFont
import tempfile
import textwrap as tw
import random
import hashlib
import threading
class Certificate():
    def __init__(self, name=None,track=None, email=None, user_id=None):
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
        name = self.name.strip()
        
        track = self.track.strip()
        


        img = Image.open("templates/template.jpg")
        width, height = img.size
        track_font = ImageFont.truetype('Vidaloka-Regular.ttf',42)

        font_name = ImageFont.truetype('Cinzel-Bold.ttf',42)        

        draw = ImageDraw.Draw(img)
    
        track_name=track.upper()
        print_name=name.upper()
        track_width, track_height=draw.textsize(track_name,font=track_font)
        name_width, name_height = draw.textsize(print_name,font=font_name)
        
        def track_draw():
            track_font = ImageFont.truetype('Vidaloka-Regular.ttf',42)
            track_width, track_height=draw.textsize(track_name,font=track_font)
            if int(track_width) >500:
                track_font = ImageFont.truetype('Vidaloka-Regular.ttf',(42*500//int(track_width)))
                track_width, track_height=draw.textsize(track_name,font=track_font)
            if int(track_width) < 250:
                track_font = ImageFont.truetype('Vidaloka-Regular.ttf', 50)                
                track_width, track_height=draw.textsize(track_name,font=track_font)
            draw.text(xy=((width-track_width)/2,(522-track_height)/2), text=track_name, fill=(166,142,70), font=track_font)   
        
        def name_draw():
            draw.text(xy=((width-name_width)/2,359+(75-name_height)/2), text=print_name, fill=(166,142,70), font=font_name)
        
        def certificate_id_draw():
            hash=hashlib.blake2b(digest_size=6)
            hash.update((str(self.user_id)+str(self.mission_id)).encode("utf-8"))
            cert_id="WID_"+hash.hexdigest()            
            cert_id_font=ImageFont.truetype('sifonn.otf',16)            
            draw.text(xy=(302,746), text=cert_id, fill=(0,0,0), font=cert_id_font)
        
     
        
        t1=threading.Thread(target=track_draw)
        t2=threading.Thread(target=name_draw)
        t3=threading.Thread(target=certificate_id_draw)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        font_name = ImageFont.truetype('Cinzel-Bold.ttf',42)        
        name_width, name_height = draw.textsize(print_name,font=font_name)
        track_width, track_height=draw.textsize(track_name,font=track_font)

        img.save( "certificates/"+self.name.replace(" ","_")+"_usr: "+str(self.user_id)+"_"+"msn:"+str(self.mission_id) +".jpg")
        # for debugging
        print("#"*40)
        print(name,width,height, name_width, name_height)
        print(track_width, track_height)
        print(self.user_id)
        print("#"*40)
if __name__=="__main__":
    cert=Certificate(name="syed ali hyder", track="quantitative modelling", email="emai", user_id=10, mission_id=10)
    cert.generate()

