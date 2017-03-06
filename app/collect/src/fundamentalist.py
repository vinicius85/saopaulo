from fundamentus import fundamentus
from elasticsearch import Elasticsearch
from datetime import datetime

def percentageToFloat(value):
  return float(value.replace('%','').replace(',','.'))

def load_input(filename):
  companies = [line.strip() for line in open(filename, 'r')]
  return companies


if __name__ == '__main__':

    es = Elasticsearch()
    es.indices.create(index='fundamental', ignore=400)

    mainStocks = load_input('/home/vinicius/workspace/saopaulo/app/collect/res/empresas.txt')

    lista = fundamentus.get_data()
    
    for k, v in lista.items():
        if(k in mainStocks):
          es.index(index="fundamental", id=k,  doc_type="stock", \
            body={
              "papel" : k, 
              "cotacao" : percentageToFloat(v['cotacao']), 
              "pl" : percentageToFloat(v['P/L']), 
              "p_vpa" : percentageToFloat(v['P/VP']), 
              "psr" : percentageToFloat(v['PSR']), 
              "div_yield": percentageToFloat(v['DY']), 
              'p_ebit' : percentageToFloat(v['P/EBIT']), 
              'ev_ebit' : percentageToFloat(v['EV/EBIT']), 
              'ebitda' : percentageToFloat(v['EBITDA']), 
              'mrg_liq' : percentageToFloat(v['Mrg.Liq.']), 
              'liq_corr' :  percentageToFloat(v['Liq.Corr.']), 
              'roic' : percentageToFloat(v['ROIC']), 
              'roe' : percentageToFloat(v['ROE']), 
              'div_brut_patr' :  percentageToFloat(v['Div.Brut/Pat.']),
              "indexUpdate": datetime.now(),
              'cres_5a' : percentageToFloat(v['Cresc.5a'])}\
          )

