import pandas as pd
import xlsxwriter

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
    return df_filtered.groupby(['NM_MUNICIPIO', 'NR_ZONA'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": 'votos_candidato'})

def tabela_cand_municipio(candidato, uf, df=data):
    df_filtered = df[(df['NM_URNA_CANDIDATO']==candidato) & (df['SG_UF']==uf)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": 'votos_candidato'})

def tabela_vv_cargo_ze(cargo, uf, df=data):
    df_filtered = df[(df['DS_CARGO']==cargo) & (df['SG_UF']==uf)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO', 'NR_ZONA'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": 'votos_validos'})

def tabela_vv_cargo_municipio(cargo, uf, df=data):
    df_filtered = df[(df['DS_CARGO']==cargo) & (df['SG_UF']==uf)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": 'votos_validos'})

def tabela_vv_cargo_partido_ze(cargo, partido, uf, df=data):
    df_filtered = df[(df['DS_CARGO']==cargo) & (df['SG_UF']==uf) & (df['SG_PARTIDO']==partido)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO', 'NR_ZONA'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": 'votos_partido'})

def tabela_vv_cargo_partido_municipio(cargo, partido, uf, df=data):
    df_filtered = df[(df['DS_CARGO']==cargo) & (df['SG_UF']==uf) & (df['SG_PARTIDO']==partido)][COLUMN_LIST]
    return df_filtered.groupby(['NM_MUNICIPIO'], as_index=False).QT_VOTOS_NOMINAIS.agg('sum').rename(columns={"QT_VOTOS_NOMINAIS": 'votos_partido'})

df_cand_ze = tabela_cand_ze(candidato, uf)
df_cand_mun = tabela_cand_municipio(candidato, uf)
df_cargo_ze = tabela_vv_cargo_ze(cargo, uf)
df_cargo_mun = tabela_vv_cargo_municipio(cargo, uf)
df_cargo_partido_ze = tabela_vv_cargo_partido_ze(cargo, partido, uf)
df_cargo_partido_mun = tabela_vv_cargo_partido_municipio(cargo, partido, uf)

df_ze = df_cand_ze.merge(df_cargo_ze, how = 'outer', on=['NM_MUNICIPIO', 'NR_ZONA']).merge(df_cargo_partido_ze, how = 'outer', on=['NM_MUNICIPIO', 'NR_ZONA']).sort_values('votos_candidato', ascending=False)
df_mun = df_cand_mun.merge(df_cargo_mun, how = 'outer', on='NM_MUNICIPIO').merge(df_cargo_partido_mun, how = 'outer', on='NM_MUNICIPIO').sort_values('votos_candidato', ascending=False)

total_votos_candidato = df_ze['votos_candidato'].sum()
total_votos_validos = df_ze['votos_validos'].sum()
total_votos_validos_nao_conquistados = total_votos_validos - total_votos_candidato

df_ze['votos válidos ainda não alcançados na ZE'] = df_ze['votos_validos'] - df_ze['votos_candidato']
df_ze['% votos do candidato'] = df_ze['votos_candidato'] / total_votos_candidato
df_ze['% votos válidos da ZE'] = df_ze['votos_candidato'] / df_ze['votos_validos']
df_ze['% votos do partido na ZE'] = df_ze['votos_candidato'] / df_ze['votos_partido']
df_ze['% votos válidos ainda não alcançados na ZE'] = df_ze['votos válidos ainda não alcançados na ZE'] / total_votos_validos_nao_conquistados

df_mun['votos válidos ainda não alcançados no Município'] = df_mun['votos_validos'] - df_mun['votos_candidato']
df_mun['% votos do candidato'] = df_mun['votos_candidato'] / total_votos_candidato
df_mun['% votos válidos do Município'] = df_mun['votos_candidato'] / df_mun['votos_validos']
df_mun['% votos do partido no Município'] = df_mun['votos_candidato'] / df_mun['votos_partido']
df_mun['% votos válidos ainda não alcançados no Município'] = df_mun['votos válidos ainda não alcançados no Município'] / total_votos_validos_nao_conquistados

writer = pd.ExcelWriter(PATH_OUT + candidato + ' - Análise.xlsx', engine='xlsxwriter')

start_row = 12

df_ze.to_excel(writer, 'ze', index=False, startrow=start_row, header=False)
df_mun.to_excel(writer, 'mun', index=False, startrow=start_row, header=False)

worksheet_ze = writer.sheets['ze']
worksheet_mun = writer.sheets['mun']

header_format = writer.book.add_format({'bold': True})
pct_format = writer.book.add_format({'num_format': '#0.00%'})

for col_num, value in enumerate(df_ze.columns.values):
    worksheet_ze.write(start_row, col_num, value, header_format)

for col_num, value in enumerate(df_mun.columns.values):
    worksheet_mun.write(start_row, col_num, value, header_format)

worksheet_ze.conditional_format(xlsxwriter.utility.xl_range(start_row, 6, start_row + len(df_ze), 9), {'type': 'no_errors', 'format': pct_format})
worksheet_ze.conditional_format(xlsxwriter.utility.xl_range(start_row, 6, start_row + len(df_ze), 6), {'type': 'data_bar', 'bar_color': '#63C384'})
worksheet_ze.conditional_format(xlsxwriter.utility.xl_range(start_row, 7, start_row + len(df_ze), 7), {'type': 'data_bar', 'bar_color': '#63C384','bar_border_color': '#63C384'})

worksheet_mun.conditional_format(xlsxwriter.utility.xl_range(start_row, 6, start_row + len(df_mun), 9), {'type': 'no_errors', 'format': pct_format})

# worksheet.conditional_format('F3:F14', {'type': 'data_bar',
#                                         'bar_color': '#63C384'})


# border_fmt = writer.book.add_format({'bottom':0, 'top':0, 'left':0, 'right':0})
# worksheet_ze.conditional_format(xlsxwriter.utility.xl_range(12, 0, 0, 100), {'type': 'no_errors', 'format': border_fmt})
# worksheet_mun.conditional_format(xlsxwriter.utility.xl_range(12, 0, 0, 100), {'type': 'no_errors', 'format': border_fmt})

writer.save()
