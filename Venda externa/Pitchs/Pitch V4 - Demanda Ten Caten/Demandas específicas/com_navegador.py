# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as BS
from time import sleep
import re
import csv

def getVotosCandidato():
    if soup.find('td', text=nome_candidato) is None:
        return 0
    else:
        return int(soup.find('td', text=nome_candidato).parent.contents[5].contents[0])

def getVotosDeLegenda():
    if soup.find('th', text=re.compile(r' - '+nome_partido+r'$')) is None:
        return [0, 0]
    else:
        considerar_votos_de_legenda = False
        votos_de_legenda = 0
        total_do_partido = 0
        for content in soup.findAll('div', {'class':'t-Region-body'})[1].contents: #todos os lugares onde existe o título de cargo
            if content.name == 'fieldset': #todos os lugares onde existe o título de cargo
                if content['class'][0] == 'area-especial':
                    if content.find('legend').contents[0] == cargo:
                        considerar_votos_de_legenda = True
                    else:
                        considerar_votos_de_legenda = False
            if considerar_votos_de_legenda:
                if content.name == 'table':
                    if content.find('th', text=re.compile(r' - '+nome_partido+r'$')) is not None:
                        votos_de_legenda = int(content.find('th', text=re.compile(r' - '+nome_partido+r'$')).parent.parent.contents[-4].contents[3].contents[0])
                        total_do_partido = int(content.find('th', text=re.compile(r' - '+nome_partido+r'$')).parent.parent.contents[-2].contents[3].contents[0])
                        return [votos_de_legenda, total_do_partido]
        return [votos_de_legenda, total_do_partido]

def getEleitores():
    eleitores_aptos = None
    comparecimento = None
    eleitores_faltosos = None
    tag_aux_1 = soup.find('th', text='Eleitores aptos')
    tag_aux_2 = soup.find('th', text='Eleitores faltosos')
    if tag_aux_1 is None:
        pass
    elif len(tag_aux_1.parent.contents)>=8:
        eleitores_aptos = int(tag_aux_1.parent.contents[3].contents[0])
        comparecimento = int(tag_aux_1.parent.contents[7].contents[0])
    if tag_aux_2 is None:
        pass
    elif len(tag_aux_2.parent.contents)>=4:
        eleitores_faltosos = int(soup.find('th', text='Eleitores faltosos').parent.contents[3].contents[0])
    return [eleitores_aptos, comparecimento, eleitores_faltosos]


def getInfos():
    soup = BS(driver.page_source, 'html.parser')
    infos = []
    infos.append(i)
    infos.append(nome_candidato)
    infos.append(mun.contents[0])
    infos.append(zona.contents[0])
    infos.append(secao.contents[0])
    infos.append(getVotosCandidato())
    infos.append(getVotosDeLegenda()[0])
    infos.append(getVotosDeLegenda()[1])
    infos.append(getEleitores()[0])
    infos.append(getEleitores()[1])
    infos.append(getEleitores()[2])
    return infos

def get_file(path_info):
    info_csv = []
    with open(path_info, 'r', newline='', encoding='cp1252') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            info_csv.append(row)
        return info_csv

def save_file(info_csv):
    with open(f"info_csv_until_{i}.csv", 'w', newline='', encoding='cp1252') as f:
        f_csv = csv.writer(f, delimiter=';')
        for line in info_csv:
            f_csv.writerow(line)
        print(f"impresso até o info_csv_until_{i}.csv")


nome_candidato = 'DIRCEU TEN CATEN'
nome_partido = 'PT'
cargo = 'Deputado Estadual'
grupo_de_impressao = 70
ultimo_numero_salvo = 2100

if ultimo_numero_salvo == 0:
    info_csv = []
    info_csv.append(['i','nome_candidato', 'municipio', 'zona', 'secao', 'votos_candidato', 'votos_de_legenda', 'total_do_partido', 'eleitores_aptos', 'comparecimento', 'eleitores_faltosos'])
else:
    info_csv = get_file(f"info_csv_until_{ultimo_numero_salvo}.csv")

i = 1

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://inter04.tse.jus.br/ords/eletse/f?p=111:1::PESQUISAR:NO:::")
driver.find_element(By.ID, "P1_UF").click()
Select(driver.find_element(By.ID, "P1_UF")).select_by_visible_text("PA")
sleep(2)
driver.find_element(By.ID, "P1_MUN").click()
sleep(2)
soup = BS(driver.page_source, 'html.parser')
sleep(2)
for mun in soup.find('select', {'id':'P1_MUN'}).findAll('option')[1:]:
    Select(driver.find_element(By.ID, "P1_MUN")).select_by_visible_text(mun.contents[0])
    sleep(2)
    driver.find_element(By.ID, "P1_ZONA").click()
    sleep(2)
    soup = BS(driver.page_source, 'html.parser')
    for zona in soup.find('select', {'id':'P1_ZONA'}).findAll('option')[1:]:
        Select(driver.find_element(By.ID, "P1_ZONA")).select_by_visible_text(zona.contents[0])
        sleep(2)
        driver.find_element(By.ID, "P1_SECAO").click()
        sleep(2)
        soup = BS(driver.page_source, 'html.parser')
        for secao in soup.find('select', {'id':'P1_SECAO'}).findAll('option')[1:]:
            Select(driver.find_element(By.ID, "P1_SECAO")).select_by_visible_text(secao.contents[0])
            if i > ultimo_numero_salvo:
                driver.find_element(By.XPATH, "//button[@id='PESQUISAR']/span[2]").click()
                sleep(3)
                soup = BS(driver.page_source, 'html.parser')
                infos = getInfos()
                info_csv.append(infos)
                if i % grupo_de_impressao == 0:
                    save_file(info_csv)
            else:
                print(f"{i} skipped")
            i+=1

save_file(info_csv)
