# Salvar a última ou penúltima região. Para que o usuário possa mandar o resto da lista de apps

import pytesseract
from pytesseract import Output
import cv2
from PIL import Image
import csv
import re
from corretor import corretor
import datetime
import os
import time

def analysis(filename):
    img= cv2.imread("./fotos/"+filename)
    img = cv2.bitwise_not(img)
    height, widht,_ = img.shape

    month = 9
    year = 2020

    # Primeiro o reconhecimento do Dia
    x1,x2,y1,y2 = 150,450, 140,200
    day = img[y1:y2, x1:x2]
    text_day = pytesseract.image_to_data(day)
    text_day = text_day.splitlines()
    texto = []
    for x,b in enumerate(text_day):
        if x!= 0:
            words = b.split()
            if (len(words)== 12):
                texto.append(words[-1])

    # Reconhecimento da Palavra Placeholder
    boxes =  (pytesseract.image_to_data(img)) 
    words = boxes.splitlines()
    for x,b in enumerate(words):
        if x!=0:
            a = b.split()
            if len (a) ==12:
                if (a[-1] == "KATEGORIEN"):
                    if  ((words[x +1].split()[-1]) == "EINBLENDEN"):
                        position = (a[6], a[7])


    # Agora o reconhecimento do horario de cada app
    # Primeiro, a definição da ROI (region of interest)
    complete_roi = img[ (int(position[1])+27) : height, 0: widht]
    height, widht,_ = complete_roi.shape
    apps_in_screen = height//77 # Quantos apps cabem na ROI escolhida. Esse número é o tamanho de cada região de APP
    apps = []
    apps_names = []

    # Timestamp position
    x1,x2,y1,y2= 105,470,38,70 

    # App Name position
    x1_app, x2_app, y1_app, y2_app = 86,350,3,40   

    # Isso varre cada região completa de um App
    for app in list(range(apps_in_screen)):
        offset = 77

        # Time recognition
        config = r'--oem 3 --psm 6 outputbase digits' # Pega só números
        ROI = complete_roi[y1:y2, x1:x2]  
        height, width,_ = ROI.shape
        boxes =  (pytesseract.image_to_data(ROI, config = config))
        words = boxes.splitlines()

        # App Name recognition
        ROI_app = complete_roi[y1_app:y2_app, x1_app:x2_app]
        height_app, width_app,_ = ROI_app.shape
        boxes_app =  (pytesseract.image_to_data(ROI_app))
        words_app = boxes_app.splitlines()

        interno = []
        interno_apps = []

        # Salva o nome do APP
        for i in range(5, len(words_app)):
            interno_apps.append(words_app[i].split()[-1])

        # Reconhecimento do tempo
        for x,b in enumerate(words):
            if x!=0:
                a = b.split()

                if len(a) == 12:
                    x,y,w,h = int(a[6]),int(a[7]),int(a[8]),int(a[9])
                    x1_1,x2_1,y1_1,y2_1 =  (w+x-85), (w+x+10), (0), (h+y+15)

                    x2 = w+x+105 + 10
                    if (x1_1 < 0):
                        x1_1 = 0

                    Small_ROI = ROI[y1_1:y2_1, x1_1:x2_1]  
                    boxes =  (pytesseract.image_to_data(Small_ROI))
                    words = boxes.splitlines()

                    # Varre a região pequena
                    for x,b in enumerate(words):
                        if x!=0:
                            a = b.split()
                            if len(a) == 12:
                                interno.append(a[-1])    

        apps_names.append(interno_apps)
        apps.append(interno)
        y1,y2, y1_app,y2_app = y1+offset, y2+offset, y1_app+offset, y2_app+offset
        
    tratado_apps, tratado = corretor(apps_names,apps)

    day =  texto[-2][:-1]+"/%s/%s"%(month, year)

    file_name = "Times.csv"
    with open (file_name, "a", newline="") as File:
        csv_file = csv.writer(File)
        # csv_file.writerow(["App", "Time","Day"])
        for i in range(0,len(apps_names)):
            csv_file.writerow( [ tratado_apps[i], tratado[i], day])

    # print ("Sucess!")


def main():
    file_name = "Times.csv"
    with open (file_name, "w", newline="") as File:
        csv_file = csv.writer(File)
        csv_file.writerow(["App", "Time","Day"])

    for filename in os.listdir("./fotos"):
        if filename.endswith(".jpeg"): 
            analysis(filename)
            
        else:
            continue

tic= time.time()

main()

toc= time.time()

tempo= str(toc-tic)

print ("Finalizado!")
print ("Tempo total: " + (tempo))

# analysis("Screentime4.jpeg")