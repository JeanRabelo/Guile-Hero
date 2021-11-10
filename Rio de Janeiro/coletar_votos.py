from bs4 import BeautifulSoup as BS
import pandas as pd
from pprint import pprint

file = open(r'Deputados estaduais eleitos no Rio de Janeiro _ Eleições 2018.html', 'r', encoding="ISO-8859-1")

soup = BS(file.read(), 'html.parser')

soup_candidatos = soup.find_all('td', {"class": "candidato"})

votos_partidos = []

for candidato in soup_candidatos:
    votos_partido = {}
    partido = candidato.find('span', {'class', 'partido'}).text
    votos = int(candidato.parent.find('span', {'class', 'qtd-votos'}).text.replace('.', '').replace(' votos', ''))
    votos_partido['partido'] = partido
    votos_partido['votos'] = votos
    votos_partidos.append(votos_partido)

to_csv = pd.DataFrame(data=votos_partidos)

to_csv.to_csv("rio dep est.csv", sep=';', encoding='ISO-8859-1')
