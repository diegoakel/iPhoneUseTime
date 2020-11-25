import re
from datetime import timedelta

# Some tests
apps = [['==', '52min'],  ['==', '28min'], ['==', '16min'], ['==', '15min'], ['==', '11min'], ['==e', 'Omin'], ['=', '5min'], ['=', '4min'], ['>', 'Amin'], ['2min'], ['Amin']]
apps_names = [['Skype'],  ['Instagram'], ['YouTube'], ['Yeelight'], ['Keep'], ['WhatsApp'], ['Forest'], ['Duolingo'], ['Notizen'], ['Jovem', 'Nerd'], ['Google', 'Notizen'], ['Bucher']]

seconds =re.compile(r'\d+s')
timeformat = re.compile(r'[\d+h]*[\d+min]*')
hour = re.compile(r'\d+h')
minutes = re.compile(r'\d+min')

def corretor(nomes, tempos):


    tratado = [] # Tempos
    tratado_apps = [] # Nomes

    apps_names = [i for i in nomes if i != []] 

    for i in tempos:
        if i == []:
            i.append("NaN")

    time,app = "",""
    
    for i in range(0, len(tempos)):
        app = (" ").join(apps_names[i])
        tratado_apps.append(app)

        if tempos[i][0] == "NaN":
            tratado.append(["NaN"])

        elif re.search(seconds, tempos[i][0]):
            tratado.append(["1min"])

        else:
            time = ("").join(tempos[i])
            time = time.lower()
            
            time  = time.replace("t", "1")
            time  = time.replace("a", "4")
            time  = time.replace("s", "5")
            time  = time.replace("q", "9")

            time = time[:-3].replace("i", "1") + time[-3:]
            tratado.append( [i for i in (re.findall(timeformat, time)) if i != ''] )

    em_minutos = []

    # Deixa em minutos
    for i in range(0, len(tratado)):
        
        if tratado[i] == []:
            tratado[i] = tratado[i-1]

        hora = re.findall(hour, tratado[i][0])
        minuto = re.findall(minutes, tratado[i][0])

        if hora != [] and minuto != []:
            atual = int("".join([s for s in hora[0] if s.isdigit()]))*60 + int("".join([s for s in minuto[0] if s.isdigit()]))

        elif hora != [] and minuto == []:
            atual = int("".join([s for s in hora[0] if s.isdigit()]))*60

        elif tratado[i][0] == "NaN":
            atual = 0

        else:
            atual = int("".join([s for s in minuto[0] if s.isdigit()]))

        em_minutos.append(atual)

    for i in range (0, len(em_minutos)):
        if i>0:
            if (em_minutos[i]> em_minutos[i-1]):
                em_minutos[i] = em_minutos[i-1]
            elif (em_minutos[i]==0):
                em_minutos[i] = em_minutos[i-1]

    tempos = []

    #Formatação
    for i in em_minutos:

        formatado = str(timedelta(minutes=i))[:-3]
        if len(formatado.split(':')[0])>1:
            formatado = formatado[1:]

        tempos.append(formatado)

    nomes = tratado_apps
    return nomes, tempos

# a,b = corretor(apps_names, apps)
