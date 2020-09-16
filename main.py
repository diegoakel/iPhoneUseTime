# Todo
# Entender a diferenca de usar ou nao cv2 no comeco pra mudar as cores
# Salvar a última ou penúltima região. Porque aí o usuário pode mandar a próxima foto sem dar erro.
# Testar várias fotos e achar os erros. Ver bibliografia de como as pessoas corrigem esses erros. Na mão msm? não sei

import pytesseract
from pytesseract import Output
import cv2
from PIL import Image

img= cv2.imread("Screentime2.jpeg")
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
apps_names = []

# Timestamp position
x1,x2,y1,y2= 92,503,35,72   

# App Name position
x1_app, x2_app, y1_app, y2_app = 86,300,3,40   


for app in list(range(apps_in_screen)):
    offset = 78
    
    # Timestamp
    ROI = complete_roi[y1:y2, x1:x2]  

    # App Name
    ROI_app = complete_roi[y1_app:y2_app, x1_app:x2_app]

    # cv2.imshow("Result", ROI_app)
    # cv2.waitKey(0)

    height, width,_ = ROI.shape

    boxes =  (pytesseract.image_to_data(ROI, config=cong))

    words = boxes.splitlines()

    

    height_app, width_app,_ = ROI_app.shape

    boxes_app =  (pytesseract.image_to_data(ROI_app))

    words_app = boxes_app.splitlines()



    interno = []

    for x,b in enumerate(words):
        if x!=0:
            a = b.split()

            app_name = words_app[x].split()
            # print (a)
            if len(a) == 12:

                # Primeiro retangulo
                x,y,w,h = int(a[6]),int(a[7]),int(a[8]),int(a[9])
                # cv2.rectangle(ROI,(x,y), (w+x, h+y), (0,0,255), 3)
                # cv2.imshow("Result", ROI)
                # cv2.waitKey(0)


                # Região definida pelo quadrado com o tamanaho do horário
                
                x1_1,x2_1,y1_1,y2_1 =  (w+x-85), (w+x+10), (0), (h+y+15)

                if (x1_1 < 0):
                    x1_1 = 0

                Small_ROI = ROI[y1_1:y2_1, x1_1:x2_1]  

                # cv2.imshow("Result", Small_ROI)
                # cv2.waitKey(0)


                boxes =  (pytesseract.image_to_data(Small_ROI))
                # boxes =  (pytesseract.image_to_data(Small_ROI, config=cong))
                words = boxes.splitlines()

                # Varre a região pequena
                for x,b in enumerate(words):
                    if x!=0:
                        a = b.split()
                        if len(a) == 12:
                            # print (a)
                            interno.append(a[-1])

                # x1,x2,y1,y2 = (w+x-56), (w+x), (8), (9)
                # print (x,y,w,h)
                # print (x,y, w+x, h+y)

            if (len(app_name) == 12):
                apps_names.append(app_name[-1])
    # cv2.imshow("Result", ROI)
    # cv2.waitKey(0)

    apps.append(interno)
    
    y1,y2 = y1+offset, y2+offset
    y1_app,y2_app = y1_app+offset, y2_app+offset



# print (apps)
# cv2.imshow("Result", complete_roi)
# cv2.waitKey(0)

# Testes de tratamento

apps = [i for i in apps if i != []] 
tratado = []
for i in apps:
    i = ("").join(i)

    # Reparos
    if (i[0] == "t" or i[0]== "T"):
        i= i.replace(i[0], "1")

    tratado.append(i)

# print (tratado)

# print (apps_names)


for i in range(0,len(apps_names)):
    print ("You spent %s on %s"%(tratado[i], apps_names[i]))