import pandas as pd

COLUMN_LIST = ['SG_UF', 'SG_UE', 'NM_UE', 'CD_MUNICIPIO', 'NM_MUNICIPIO', 'NR_ZONA', 'DS_CARGO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', 'TP_AGREMIACAO', 'NR_PARTIDO', 'SG_PARTIDO', 'NM_COLIGACAO', 'DS_COMPOSICAO_COLIGACAO', 'DS_SIT_TOT_TURNO', 'QT_VOTOS_NOMINAIS']

PATH_IN = r'C:\Users\jean_\Downloads\votacao_candidato_munzona_2018 (4)\votacao_candidato_munzona_2018_BRASIL.csv'
data = pd.read_csv(PATH_IN, encoding = 'ISO-8859-1', sep=';')
PATH_OUT = r'C:\Users\jean_\Documents\GitHub\Guile Hero\Venda externa\Pitchs\Pitch V3 - Próximo\\'[:-1]

candidato = 'JOAQUIM PASSARINHO'
uf = 'PA'
partido = 'PSD'
cargo = 'Deputado Federal'

def tabela_cand_ze(candidato, uf, df=data):
    df_filtered = df[(df['NM_URNA_CANDIDATO']==candidato) & (df['SG_UF']==uf)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO', 'NR_ZONA'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": "votos_candidato"})

def tabela_cand_municipio(candidato, uf, df=data):
    df_filtered = df[(df['NM_URNA_CANDIDATO']==candidato) & (df['SG_UF']==uf)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": "votos_candidato"})

def tabela_vv_cargo_ze(cargo, uf, df=data):
    df_filtered = df[(df['DS_CARGO']==cargo) & (df['SG_UF']==uf)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO', 'NR_ZONA'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": "votos_validos"})

def tabela_vv_cargo_municipio(cargo, uf, df=data):
    df_filtered = df[(df['DS_CARGO']==cargo) & (df['SG_UF']==uf)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": "votos_validos"})

def tabela_vv_cargo_partido_ze(cargo, partido, uf, df=data):
    df_filtered = df[(df['DS_CARGO']==cargo) & (df['SG_UF']==uf) & (df['SG_PARTIDO']==partido)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO', 'NR_ZONA'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": "votos_partido"})

def tabela_vv_cargo_partido_municipio(cargo, partido, uf, df=data):
    df_filtered = df[(df['DS_CARGO']==cargo) & (df['SG_UF']==uf) & (df['SG_PARTIDO']==partido)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": "votos_partido"})

df_cand_ze = tabela_cand_ze(candidato, uf)
df_cand_mun = tabela_cand_municipio(candidato, uf)
df_cargo_ze = tabela_vv_cargo_ze(cargo, uf)
df_cargo_mun = tabela_vv_cargo_municipio(cargo, uf)
df_cargo_partido_ze = tabela_vv_cargo_partido_ze(cargo, partido, uf)
df_cargo_partido_mun = tabela_vv_cargo_partido_municipio(cargo, partido, uf)

df_ze = df_cand_ze.merge(df_cargo_ze, how = 'outer', on=['NM_MUNICIPIO', 'NR_ZONA']).merge(df_cargo_partido_ze, how = 'outer', on=['NM_MUNICIPIO', 'NR_ZONA']).sort_values('votos_candidato', ascending=False)
df_mun = df_cand_mun.merge(df_cargo_mun, how = 'outer', on='NM_MUNICIPIO').merge(df_cargo_partido_mun, how = 'outer', on='NM_MUNICIPIO').sort_values('votos_candidato', ascending=False)

writer = pd.ExcelWriter(PATH_OUT + candidato + ' - Análise.xlsx')

df_ze.to_excel(writer, 'ze')
df_mun.to_excel(writer, 'mun')

writer.save()
