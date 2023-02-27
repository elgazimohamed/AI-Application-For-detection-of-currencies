import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras import applications
import numpy as np
import matplotlib.pyplot as plt
import cv2
import PySimpleGUI as sg
from PIL import Image
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import PIL.Image
from PIL import Image,ImageTk
import numpy

model = tf.keras.models.load_model('model.h5')
 
class_names = ['10 DH', '10 centime', '10 franc', '1DH', '1 centime', '1 euro',
               '20 centime', '20 franc', '2 DH', '2 centime', '2 euro',
               '50 centime', '50 franc', '5DH', '5 centime']

my_w = tk.Tk()
my_w.geometry("1350x650")  # Size of the window 
my_w.title('Application de Detection des monnaies')
my_font1=('times', 18, 'bold')

l1 = tk.Label(my_w,text='original',width=30,font=my_font1)  
l1.grid(row=1,column=1)

l2 = tk.Label(my_w,text='resultat',width=30,font=my_font1)  
l2.grid(row=1,column=2)

l3 = tk.Label(my_w,text='',width=30,font=my_font1)  
l3.grid(row=3,column=3)

b1 = tk.Button(my_w, text='selectionner fichier', 
   width=20,command = lambda:upload_file())
b1.grid(row=2,column=1)

b2 = tk.Button(my_w, text='executer', 
   width=20,command = lambda:exe())
b2.grid(row=2,column=2) 



def exe():
    global img,pic,pimg,l3

    class_counter=[0]*15

    gray = cv2.cvtColor(pic,cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray,9)

    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,0.95,400,
                            param1=85,param2=85,minRadius=100,maxRadius=700)
    h, w, _ = pic.shape                        
    count=0
    pic=cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    for i in circles[0,:]:
        
        minx=int(i[1])-int(i[2])-10
        maxx=int(i[1])+int(i[2])+10
        miny=int(i[0])-int(i[2])-10
        maxy=int(i[0])+int(i[2])+10

        if(int(i[1])-int(i[2])-10<0):
            minx=1
        if(int(i[1])+int(i[2])+10>h):
            maxx=h-1
        if(int(i[0])-int(i[2])-10<0):
            miny=1
        if(int(i[0])+int(i[2])+10>w):
            maxy=w-1

        cropped_image = pic[minx:maxx,miny:maxy]
        cropped_image = cv2.resize(cropped_image,(150,150))

        nbr=np.argmax(model.predict([cropped_image.reshape(-1,150,150,3)]))
        class_counter[nbr]=class_counter[nbr]+1
        cv2.imwrite('C:/Users/A CER/Desktop/Projects/output/img'+str(count)+'.jpg', cropped_image)    
        cv2.circle(pic,(int(i[0]),int(i[1])),int(i[2]),(255,0,0),10)
        
        count=count+1

    
    color_coverted = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(color_coverted)
    img_resized=img.resize((350,550))
    img=ImageTk.PhotoImage(img_resized)

    b2 =tk.Button(my_w,image=img) # using Button 
    b2.grid(row=3,column=2)

    tot=""
    for i in range(15):
        if(class_counter[i]!=0):
            tot=tot+("il y a "+str(class_counter[i])+" de piece de valeur de "+class_names[i])+"\n"
    
    l3.config(text=tot)

    
 

def upload_file():
    global img,pic,pimg
    f_types = [('Jpg Files', '*.jpg;*.jpeg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    pic=plt.imread(filename)
    img=Image.open(filename)
    img_resized=img.resize((350,550))
    pimg=ImageTk.PhotoImage(img_resized)
    b2 =tk.Button(my_w,image=pimg) # using Button 
    b2.grid(row=3,column=1)

my_w.mainloop()  # Keep the window open