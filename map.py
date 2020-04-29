from matplotlib import pyplot as plt
import csv
import math
import numpy as np
#maks to 153.832040129247
#min to 43.2528741577922
def addVectors(a,b):
    x = a[0] + b[0]
    y = a[1] + b[1]
    z = a[2] + b[2]
    return [x,y,z]
def float2rgb(height,maksimum,min):
    blue=0.0
    green = 1.0 - (height-min)/(maksimum-min)
    red = (height-min)/(maksimum-min)
    return [red,green,blue]

def rgb2hsv(rgb):
    #r, g, b = r/255.0, g/255.0, b/255.0
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return [h, s, v]

def hsv2rgb(hsv):
    h = float(hsv[0])
    s = float(hsv[1])
    v = float(hsv[2])
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    return [r, g, b]

def rgb2hsv2rgb(rgbArr,kosinus):
    HSVarr = rgb2hsv(rgbArr)
    if kosinus>0.0:
        HSVarr[2] = kos * 4.5
        HSVarr[1] = 1.0 - 1.2*kos
    else:
        HSVarr[2] = abs(kos)
        HSVarr[1] = 1.0  - abs(kos)
    RGBarr2 = hsv2rgb(HSVarr)
    return RGBarr2

def cosinus(sunVec,pointVec):
    skalarny = sunVec[0]*pointVec[0]+sunVec[1]*pointVec[1]+sunVec[2]*pointVec[2]
    sunVecLen = math.sqrt(sunVec[0]**2+sunVec[1]**2+sunVec[2]**2)
    pointVecLen = math.sqrt(pointVec[0]**2+pointVec[1]**2+pointVec[2]**2)
    kosinus = skalarny/(sunVecLen*pointVecLen)
    return kosinus

def sun2pixelVec(sunVec,pixelVec):
    # x = pixelVec[0]-sunVec[0]
    # y = pixelVec[1]-sunVec[1]
    # z = pixelVec[2]-sunVec[2]
    x = sunVec[0]-pixelVec[0]
    y = sunVec[1]-pixelVec[1]
    z = sunVec[2]-pixelVec[2]
    vecLen = math.sqrt(x**2+y**2+z**2)
    x = x/vecLen
    y = y/vecLen
    z = z/vecLen
    return [x,y,z]

def normal(a,b):
    ax = a[0]
    ay = a[1]
    az = a[2]
    bx = b[0]
    by = b[1]
    bz = b[2]
    # wspolrzedne wektora normalnego
    x = ay*bz - az*by
    y = az*bx - ax*bz
    z = ax*by - ay*bx
    # normalizacja wektora normalnego
    # normalVecLen = math.sqrt(x**2+y**2+z**2)
    # x = x/normalVecLen
    # y = y / normalVecLen
    # z = z / normalVecLen
    return [x,y,z]


with open ('big.dem','r') as csvfile:
        dane = []
        plots = csv.reader(csvfile, delimiter=' ')
        row_num = 0
        tablica_wektorow = []
        y = 0 #w ktorym wierszu aktualnie jestem
        for wiersz in plots:
                x = 0 #w ktorym elemencie w wierszu jestem
                wiersz_wektorow = []
                if row_num>0:
                    wiersz.pop(500)
                    kolorki = [float2rgb(float(i),153.832040129247,43.2528741577922) for i in wiersz]
                    for element in wiersz:
                        wiersz_wektorow.append([x*7537/100,y*7537/100,float(element)]) # x y z(height)
                        x = x + 1
                    dane.append(kolorki)
                    tablica_wektorow.append(wiersz_wektorow)
                    y = y + 1
                row_num = row_num + 1

tablica_normalnych = []
wiersz_normalnych = []
for y in range(500):
    wiersz_normalnych = []
    for x in range(500):
        if y==0 or x==0 or x==499 or y==499:
            wiersz_normalnych.append([1.0,1.0,1.0])
        else:
            #aktualnie liczony punkt
            actualVec = tablica_wektorow[y][x]
            #lewo i gora (gora x lewo )
            nearbyVec1 = tablica_wektorow[y][x - 1] #lewo
            nearbyVec2 = tablica_wektorow[y - 1][x] #gora
            a1 = [nearbyVec1[0] - actualVec[0],nearbyVec1[1] - actualVec[1],nearbyVec1[2] - actualVec[2]] #lewo
            b1 = [nearbyVec2[0] - actualVec[0],nearbyVec2[1] - actualVec[1],nearbyVec2[2] - actualVec[2]] #gora
            #prawo i w dol ( dol x prawo)
            nearbyVec3 = tablica_wektorow[y + 1][x] #dol
            nearbyVec4 = tablica_wektorow[y][x + 1] #prawo
            a2 = [nearbyVec3[0] - actualVec[0],nearbyVec3[1] - actualVec[1],nearbyVec3[2] - actualVec[2]] #dol
            b2 = [nearbyVec4[0] - actualVec[0],nearbyVec4[1] - actualVec[1],nearbyVec4[2] - actualVec[2]] #prawo
            #wyliczenie normalnych i ich wypadkowej
            normal1 = normal(a1,b1)
            normal2 = normal(b2,a2)
            normalna = addVectors(normal1,normal2) #wypadkowa normalnych

            #normalizacja
            normalnaLen = math.sqrt(normalna[0] ** 2 + normalna[1] ** 2 + normalna[2] ** 2)
            normalna[0] = normalna[0] / normalnaLen
            normalna[1] = normalna[1] / normalnaLen
            normalna[2] = normalna[2] / normalnaLen



            wiersz_normalnych.append(normalna)

    tablica_normalnych.append(wiersz_normalnych)


x = 0
y = 0
tablica_koncowa = []
wektor_slonca = [-40000.0,15000.0,10000.0]
for y in range(500):
    wiersz_koncowy = []
    for x in range(500):
        rgArr = dane[y][x]
        normalny = tablica_normalnych[y][x]
        kos = cosinus(sun2pixelVec(wektor_slonca,tablica_wektorow[y][x]),normalny)
        wiersz_koncowy.append(rgb2hsv2rgb(rgArr,kos))
    tablica_koncowa.append(wiersz_koncowy)





plt.tick_params(top=True, right=True, direction='in')
plt.imshow(tablica_koncowa)
plt.show()

