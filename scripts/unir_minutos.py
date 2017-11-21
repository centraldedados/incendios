#!/usr/bin/env python3
import csv
import sys

filename = sys.argv[1]
reader = csv.DictReader(open(filename, 'r'))
#if 'minutos_inicio' not in list(reader)[0]:
#    sys.exit()

fieldnames = ['ano', 'codigo_sgif', 'observ', 'concelho', 'freguesia', 'data_inicio', 'hora_inicio', 'data_fim', 'hora_fim', 'area_arborizada', 'area_nao_arborizada', 'area_total', 'causa']

writer = csv.DictWriter(open(filename.replace('.csv', '-new.csv'), 'w'), fieldnames=fieldnames)
writer.writeheader()
for row in reader:
    if not row.get('minutos_inicio'):
        sys.exit()
    new_row = dict(row)

    min_inicio = new_row['minutos_inicio']
    min_fim = new_row['minutos_fim']
    if len(str(min_inicio)) == 1:
        min_inicio = '0' + str(min_inicio)
    if len(str(min_fim)) == 1:
        min_fim = '0' + str(min_fim)

    new_row['hora_inicio'] = new_row['hora_inicio'] + ':' + min_inicio
    new_row['hora_fim'] = new_row['hora_fim'] + ':' + min_fim
    new_row.pop('minutos_inicio')
    new_row.pop('minutos_fim')
    writer.writerow(new_row)
