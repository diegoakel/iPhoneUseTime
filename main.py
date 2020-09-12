# Todo
#- Entender a diferenca de usar ou nao cv2 no comeco pra mudar as cores
# continuar em 19:11 aqui: https://www.youtube.com/watch?v=6DjFscX4I_c
# botar pra fechar o "while" se achar: "ValueError: tile cannot extend outside image"

import pytesseract
from pytesseract import Output
import cv2
from PIL import Image

img= cv2.imread("Screentime.jpeg")
img = cv2.bitwise_not(img)
height, widht,_ = img.shape

# Primeiro o reconhecimento do placeholder
boxes =  (pytesseract.image_to_data(img)) 
words = boxes.splitlines()

for x,b in enumerate(words):
    if x!=0:
        a = b.split()
        # print (a)
        if len (a) ==12:
            if (a[-1] == "KATEGORIEN"):
                if  ((words[x +1].split()[-1]) == "EINBLENDEN"): #& ((words[x +2][-1]) == "APP") )
                    position = (a[6], a[7])


# Agora o reconhecimento do horario de cada app

# Isso é tudo abaixo da palavra PlaceHolder
complete_roi = img[ (int(position[1])+27) : height, 0: widht]

height, widht,_ = complete_roi.shape
apps_in_screen = height//77 # Quantos apps cabem na ROI escolhida. Esse número é o tamanho de cada região de APP

cong = r'--oem 3 --psm 6 outputbase digits'
apps = []

x1,x2,y1,y2= 92,503,40,70   

for app in list(range(apps_in_screen)):
    offset = 77
    
    ROI = complete_roi[y1:y2, x1:x2]  

    height, width,_ = ROI.shape


    boxes =  (pytesseract.image_to_data(ROI, config=cong))
    # cv2.imshow("Result", ROI)
    # cv2.waitKey(0)

    # boxes =  (pytesseract.image_to_data(complete_roi, config=cong))
    words = boxes.splitlines()


    interno = []

    for x,b in enumerate(words):
        if x!=0:
            a = b.split()
            print (a)
            if len(a) == 12:
                # Primeiro retangulo
                x,y,w,h = int(a[6]),int(a[7]),int(a[8]),int(a[9])
                # cv2.rectangle(ROI,(x,y), (w+x, h+y), (0,0,255), 3)
                # cv2.imshow("Result", ROI)
                # cv2.waitKey(0)

                x1,x2,y1,y2 = (w+x-86), (w+x), (y-2), (h+10)
                # Região definida pelo quadrado com o tamanaho do horário
                # Small_ROI = ROI[y:height, x:width]  
                Small_ROI = ROI[y1:y2, x1:x2]  

                cv2.imshow("Result", Small_ROI)
                cv2.waitKey(0)


                boxes =  (pytesseract.image_to_data(Small_ROI, config=cong))
                words = boxes.splitlines()

                # Varre a região pequena
                for x,b in enumerate(words):
                    if x!=0:
                        a = b.split()
                        print (a)
                        if len(a) == 12:
                            interno.append(a[-1])

                # x1,x2,y1,y2 = (w+x-56), (w+x), (8), (9)
                # print (x,y,w,h)
                # print (x,y, w+x, h+y)

    # cv2.imshow("Result", ROI)
    # cv2.waitKey(0)

    apps.append(interno)
    
    y1,y2 = y1+offset, y2+offset



# cv2.imshow("Result", complete_roi)
# cv2.waitKey(0)