import csv

# PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_AP.csv'
# PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_SP.csv'
PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_BRASIL.csv'

dados = open(PATH_IN,'r')
dados_csv = csv.reader(dados, delimiter=';')

for i in range(0,10):
    print(next(dados_csv))
