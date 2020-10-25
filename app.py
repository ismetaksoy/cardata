# Libraries to import
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import sqlite3


# variabelen die in excel komen te staan
merkmodel = []
bouwjaar = []
uitvoering = []
kmstand = []
carroserie = []
kenteken = []
apk = []
brandstof = []
kmstand = []
energielabel = []
verbruik = []
prijs = []
linkadv = []
datumadv = []

for page in range(1):
    # basis link die we plakken aan de link die we minen
    base = 'https://www.marktplaats.nl'
    
    link = f"https://www.marktplaats.nl/l/auto-s/bmw/p/{page}/"
    data = requests.get(link)
    # parsen van de pagina in html om daaruit de gegevens uit te halen
    soup = BeautifulSoup(data.content,"html.parser")
    
    # hier staat iedere advertentie per pagina. Per pagina zijn dat 34 ads
    car = soup.findAll('li',{'class':'mp-Listing mp-Listing--list-item'})
    # in deze variabelen slaan we per advertentie de kerngegevens op om ze vervolgens op te halen en in de variabelen
    # bovenin op te nemen
    value = []

    for i in range(len(car)):
        # uit de car variabelen minen we de urls van de advertenties om deze een voor een te bezoeken en de gegevens te minen.
        autolink = base+car[i].a['href']
        # we minen hier de link van de advertentie zodat we deze later direct kunnen bezoeken
        linkadv.append(autolink)
        data_car = requests.get(autolink)
        # hier parsen we de advertentiepagina om gegevens eruit te halen
        soupdata = BeautifulSoup(data_car.content,'html.parser')
        # specs = soupdata.findAll('div',{'class':'spec-table-item'})
        
        keyspecs = soupdata.findAll('span',{'class':'key'})
        # valuespecs minet alle data die in de tabel staat met de kerngegevens
        valuespecs = soupdata.findAll('span',{'class':'value'})
        # we slaan al deze gegevens op in de value variabelen
        value.append(valuespecs)
        
        # per advertentie minen we de datum waarop de advertentie is geplaatst op markplaats. 
        gezien = soupdata.find('span',{'id':'displayed-since'})
        datum = list(gezien)[5]
        datumgeplaatst = str(datum)[6:-7]
        datumadv.append(datumgeplaatst)
for i in range(len(value)):
        try:
    # in de value variabelen slaan we per advertentie de brongegevens op en halen deze op. op nummer 0 staat bijv merk en model
            merkmodel.append(str(value[i][0])[20:-7])
        except: 
            merkmodel.append('Not available')
        try:
            bouwjaar.append(str(value[i][1])[20:-7])
        except:
            bouwjaar.append('Not available')
        try:
            uitvoering.append(str(value[i][2])[20:-7])
        except:
            uitvoering.append('Not available')
        try:    
            carroserie.append(str(value[i][3])[20:-7])
        except:
            carroserie.append('Not available')
        try:
            kenteken.append(str(value[i][4])[20:-7])
        except:
            kenteken.append('Not available')
        try:
            apk.append(str(value[i][5])[20:-7])
        except:
            apk.append('Not available')
        try:
            brandstof.append(str(value[i][6])[20:-7])
        except:
            brandstof.append('Not available')
        try:
            kmstand.append(str(value[i][7])[20:-7])
        except:
            kmstand.append('Not available')
        try:
            energielabel.append(str(value[i][9])[20:-7])
        except:
            energielabel.append('Not available')
        try:
            verbruik.append(str(value[i][10])[20:-7])
        except:
            verbruik.append('Not available')
        try:
            prijs.append(str(value[i][11])[20:-7])
        except:
            prijs.append('Not available')
data = {
    'merkmodel':merkmodel,
    'link':linkadv,
    'bouwjaar':bouwjaar,
    'uitvoering':uitvoering,
    'carroserie':carroserie,
    'kenteken':kenteken,
    'apk':apk,
    'brandstof':brandstof,
    'kmstand':kmstand,
    'energielabel':energielabel,
    'verbruik':verbruik,
    'prijs':prijs,
    'datum advertentie':datumadv
}

df = pd.DataFrame(data)

df.to_csv('bmw.csv')