# Libraries to import
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

base = "https://www.marktplaats.nl"
link = "https://www.marktplaats.nl/l/auto-s/bmw"
data = requests.get(link)

# parsen van de pagina in html om daaruit de gegevens uit te halen
soup = BeautifulSoup(data.content, "html.parser")

# Vind alle advertenties op marktplaats
advertentie = soup.find_all('li',{'class':'mp-Listing mp-Listing--list-item'})

# Sla de links naar de advertenties op in de variabele advertentie_link
advertentie_link = []
for i in range(len(advertentie)):
	advertentie_link.append(base+advertentie[i].a['href'])
