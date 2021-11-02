import pandas as pd

# PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_AP.csv'
# PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_RS.csv'
# PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_SP.csv'
PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_BRASIL.csv'
data = pd.read_csv(PATH_IN, encoding = "ISO-8859-1", sep=";")
print(data.head())
print(PATH_IN)

# salvar parte do Eduardo Bolsonaro
data[data["NM_URNA_CANDIDATO"]=="EDUARDO BOLSONARO"].to_csv("Eduardo Bolsonaro.csv", sep=';', encoding='ISO-8859-1')
# salvar parte da Joice Hasselmann
data[data["NM_URNA_CANDIDATO"]=="JOICE HASSELMANN"].to_csv("choice.csv", sep=';', encoding='ISO-8859-1')
# salvar parte do Kim
data[data["NM_URNA_CANDIDATO"]=="KIM KATAGUIRI"].to_csv("kim basinger.csv", sep=';', encoding='ISO-8859-1')
