import pandas as pd

COLUMN_LIST = ["SG_UF", "SG_UE", "NM_UE", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "DS_CARGO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "TP_AGREMIACAO", "NR_PARTIDO", "SG_PARTIDO", "NM_COLIGACAO", "DS_COMPOSICAO_COLIGACAO", "DS_SIT_TOT_TURNO", "QT_VOTOS_NOMINAIS"]

PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_BRASIL.csv'
data = pd.read_csv(PATH_IN, encoding = "ISO-8859-1", sep=";")

def save_csv(candidato, df=data):
    df[df["NM_URNA_CANDIDATO"]==candidato][COLUMN_LIST].to_csv(candidato + ".csv", sep=';', encoding='ISO-8859-1')

save_csv("EDUARDO BOLSONARO")
save_csv("JOICE HASSELMANN")
save_csv("KIM KATAGUIRI")

data[['SG_PARTIDO', 'NM_PARTIDO', 'NM_COLIGACAO', 'DS_COMPOSICAO_COLIGACAO']].drop_duplicates(['SG_PARTIDO', 'NM_PARTIDO', 'NM_COLIGACAO', 'DS_COMPOSICAO_COLIGACAO'],keep= 'last').to_csv("partidos e coligações.csv", sep=';', encoding='ISO-8859-1')

data.groupby(['NM_UE', 'SG_PARTIDO', 'NM_PARTIDO', 'NM_COLIGACAO', 'DS_COMPOSICAO_COLIGACAO']).QT_VOTOS_NOMINAIS.agg('sum')
data[data['DS_CARGO']=='Deputado Federal'].groupby(['NM_UE', 'SG_PARTIDO', 'NM_PARTIDO', 'NM_COLIGACAO', 'DS_COMPOSICAO_COLIGACAO'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').to_csv("group by partido dep fed.csv", sep=';', encoding='ISO-8859-1')
data[data['DS_CARGO']=='Deputado Estadual'].groupby(['NM_UE', 'SG_PARTIDO', 'NM_PARTIDO', 'NM_COLIGACAO', 'DS_COMPOSICAO_COLIGACAO'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').to_csv("group by partido dep fed.csv", sep=';', encoding='ISO-8859-1')
