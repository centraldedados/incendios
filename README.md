# 🔥 Incêndios em Portugal

## Fontes

Os dados históricos de incêndios florestais foram retirados do [ICFN - Instituto da conversão da Natureza e Florestas](http://www.icnf.pt/portal/florestas/dfci/inc/estat-sgif).

## Edições e melhorias

Fizemos bastantes melhoramentos e edições aos datasets originais; tentamos
elencar aqui as alterações mais importantes:

* Datas em formato ISO 8601, ano-mês-dia (`YYYY-MM-DD`)
* Harmonizar os nomes das colunas
* Apagar entradas desnecessárias
* Remover aspas desnecessárias (_quote characters_)
* Remover horas vazias dos campos de data
* Unificar colunas de horas e minutos numa coluna de hora única
* Eliminação de valores `NULL`
* Consertar as terminações de linha e codificação UTF-8

## Resources

* [Analysis of fields](fields.md): result of analysis of fields
* [csv_tool.py](scripts/csv_tool.py): script to analyse and merge collection of CSV files
* [merged.csv](data/merged.csv): CSV merged with csv_tool.py

### Merging CSV files

Para juntar os vários CSV é preciso incluir o ano, que pode ser retirado do nome do ficheiro 
(uma vez que não está incluído em todos os CSV). Como ninguém nos impede, podemos
ser preguiçosos e incluir logo código Python directamente na linha de comandos:

```
$ scripts/csv_tool.py merge data/incendios*.csv -e "lambda f: dict(ano=re.match('.*incendios(\d{4}).csv', f.name)[1])" -o data/merged.csv
```

Este código usa uma expressão regular para extrair o `ano` do nome do ficheiro:

```python
lambda f: dict(ano=re.match('.*incendios(\d{4}).csv', f.name)[1])
```

## Referências

### Outras fontes sobre incêndios

- [Cartografia da área
  ardida](http://www.icnf.pt/portal/florestas/dfci/inc/info-geo) em formato
  Shapefile, que é possível associar a outros dados (por exemplo, da ANPC) pelo
  código de ocorrência (COD_OCO)
- O repositório da [Proteção
  Civil](https://github.com/centraldedados/protecao_civil) contém a informação
  em tempo real de ocorrências, sendo que podemos filtrar as entradas por
  natureza (exemplo: Incêndios Rurais)

### Outros datasets

- [Boletim de trânsito, com estradas cortadas](http://www.estradas.pt/Informacoes/Boletim-de-Transito)
- [Qualidade do ar](http://qualar.apambiente.pt/)
- [Pontos de Água](http://fogos.icnf.pt/sgif2010/)
- [Risco de incêndio](http://www.ipma.pt/en/ambiente/risco.incendio/index.jsp)
- [Corpos de Bombeiros](https://www.bombeiros.pt/mapa/)

### Outros websites

- [Fogos.pt](https://fogos.pt/)
- [Incêndios](http://incendios.pt/)
- [EFFIS - European Forest Fire Information System](http://effis.jrc.ec.europa.eu/)
- [PORDATA - Incêndios florestais e área ardida](https://www.pordata.pt/Portugal/Inc%C3%AAndios+florestais+e+%C3%A1rea+ardida+%E2%80%93+Continente-1192)
- [Não aos fogos](http://naoaosfogos.pt/)
