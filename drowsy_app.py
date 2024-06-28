import tkinter as tk 
import customtkinter as ctk
import torch 
import numpy as np
import cv2
from PIL import Image,ImageTk
import vlc
import random
app = tk.Tk()
app.geometry("600x600")
app.title("Drowsy boi 4.0")
ctk.set_appearance_mode("dark")

vidFrame = tk.Frame(height=480 ,width=600)
vidFrame.pack()
vid= ctk.CTkLabel(vidFrame)
vid.pack()
counter =0
counterLabel = ctk.CTkLabel(master=app,text=counter,height=40 , width=120,text_color="white",fg_color="teal")
counterLabel.pack(pady=10)
def reset_counter():
    global counter
    counter =0

resetbutton  = ctk.CTkButton(master=app,text="reset counter",command = reset_counter,height=40 , width=120,text_color="white",fg_color="teal")  
resetbutton.pack()
model = torch.hub.load('ultralytics/yolov5','custom',path='yolov5/runs/train/exp27/weights/last.pt',force_reload=True)

cap = cv2.VideoCapture(0)

def detect():
    global counter
    ret,frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results= model(frame)
    img = np.squeeze(results.render())
    print(results.xywh[0])
    if len(results.xywh[0]) >0:
      
        dconf =results.xywh[0][0][4]
        dclass = results.xywh[0][0][5]
        # dconf.item()>0.85 and
        if dclass.item() == 16.00000:
           counter +=1
           counterLabel.configure(text=counter)
        #    fielchoice = random.choice([1,2,3])
           if(counter>20):
            p= vlc.MediaPlayer(f"file:///alarm-clock-beep-105903.mp3")
            p.play()
            counter=0       
    imgarr = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(imgarr)
    vid.imgtk = imgtk
    vid.configure(image=imgtk)
    vid.after(10,detect)
    # counterLabel.configure(text=counter)
detect()
app.mainloop()