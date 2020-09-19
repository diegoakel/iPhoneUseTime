# Todo
# Entender a diferenca de usar ou nao cv2 no comeco pra mudar as cores
# Salvar a última ou penúltima região. Porque aí o usuário pode mandar a próxima foto sem dar erro.
# Testar várias fotos e achar os erros. Ver bibliografia de como as pessoas corrigem esses erros. Na mão msm? não sei
# Limpar tudo. Nomes de vars e etc e fazer commit publico.
# No Screentime4 ele não pegou o penúltimo (classroom)
# Trocando 5 por S. 
# Fazer ele acumular o aprendizado. 


import pytesseract
from pytesseract import Output
import cv2
from PIL import Image
import csv

img= cv2.imread("Screentime2.jpeg")
img = cv2.bitwise_not(img)
height, widht,_ = img.shape

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

cong = r'--oem 3 --psm 6 outputbase digits'
apps = []
apps_names = []

# Timestamp position
x1,x2,y1,y2= 92,503,35,72   

# App Name position
x1_app, x2_app, y1_app, y2_app = 86,350,3,40   

# Isso varre cada região completa de um App
for app in list(range(apps_in_screen)):
    offset = 78

    # Time recognition
    ROI = complete_roi[y1:y2, x1:x2]  
    height, width,_ = ROI.shape
    boxes =  (pytesseract.image_to_data(ROI, config=cong)) # Tirar esse cong daq
    words = boxes.splitlines()

    # App Name recognition
    ROI_app = complete_roi[y1_app:y2_app, x1_app:x2_app]
    height_app, width_app,_ = ROI_app.shape
    boxes_app =  (pytesseract.image_to_data(ROI_app))
    words_app = boxes_app.splitlines()

    # cv2.imshow("Result", ROI_app)
    # cv2.waitKey(0)

    interno = []
    interno_apps = []

    for x,b in enumerate(words):
        if x!=0:
            # Time
            a = b.split()
            # Apps
            app_name = words_app[x].split()
            
            if len(a) == 12:

                # Quadrado de reconhecimento
                x,y,w,h = int(a[6]),int(a[7]),int(a[8]),int(a[9])
                # cv2.rectangle(ROI,(x,y), (w+x, h+y), (0,0,255), 3)
                # cv2.imshow("Result", ROI)
                # cv2.waitKey(0)

                # Região definida pelo quadrado com o tamanaho do horário
                x1_1,x2_1,y1_1,y2_1 =  (w+x-85), (w+x+10), (0), (h+y+15)

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

            if (len(app_name) == 12):
                x,y,w,h = int(app_name[6]),int(app_name[7]),int(app_name[8]),int(app_name[9])
                x1_1,x2_1,y1_1,y2_1 =  (0), (w+x+100), (0), (h+y+15)

                Small_ROI = ROI_app[y1_1:y2_1, x1_1:x2_1]  
                boxes =  (pytesseract.image_to_data(Small_ROI))
                words = boxes.splitlines()

                for x,b in enumerate(words):
                    if x!=0:
                        a = b.split()
                        if len(a) == 12:
                            interno_apps.append(a[-1])

    apps_names.append(interno_apps)
    apps.append(interno)

    y1,y2, y1_app,y2_app = y1+offset, y2+offset, y1_app+offset, y2_app+offset
    

# Limpar de Vazios
apps_names = [i for i in apps_names if i != []] 
apps = [i for i in apps if i != []] 

tratado = []
tratado_apps = []
time,app = "",""

for i in range(0, len(apps)):
    time = ("").join(apps[i])
    app = (" ").join(apps_names[i])

    # Reparos
    if (time[0] == "t" or time[0]== "T"):
        time= time.replace(time[0], "1")

    tratado.append(time)
    tratado_apps.append(app)

file_name = "Times.csv"
with open (file_name, "w", newline="") as File:
    csv_file = csv.writer(File)
    csv_file.writerow(["App", "Time","Day"])
    for i in range(0,len(apps_names)):
        csv_file.writerow( [ tratado_apps[i], tratado[i], texto[-2]+texto[-1]])
