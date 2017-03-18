from fundamentus import fundamentus
from elasticsearch import Elasticsearch
from datetime import datetime
from math import log

def percentageToFloat(value):
  return float(value.replace('%','').replace(',','.'))

def load_input(filename):
  companies = [line.strip() for line in open(filename, 'r')]
  return companies

def load_companies_info(filename):
  dict = {}
  companies = [line.strip() for line in open(filename, 'r')]
  for company in companies:
    companyData = company.split(';')
    dict.update({companyData[0]:{'nome' :    companyData[1],
                                 'setor':    companyData[2],
                                 'subsetor': companyData[3],
                                 'segmento': companyData[4]}})
  return dict


def compute_score(att):
  p_vpa = percentageToFloat(att['P/VP']) 
  d_y = percentageToFloat(att['DY']) 
  roe = percentageToFloat(att['ROE']) 
  return   (- 10 * p_vpa) + (2 * d_y) + roe
         


if __name__ == '__main__':

    es = Elasticsearch()
    es.indices.create(index='fundamental', ignore=400)

    mainStocks = load_companies_info('/home/vinicius/workspace/saopaulo/app/collect/res/empresas.txt')
    lista = fundamentus.get_data()

    ### Incluir carteira
    
    for k, v in lista.items():
        if(k in mainStocks):
          es.index(index="fundamental", id=k,  doc_type="stock", \
            body={
              "papel" : k, 
              "nome" : mainStocks.get(k)['nome'],
              "setor" : mainStocks.get(k)['setor'],
              "subsetor" : mainStocks.get(k)['subsetor'],
              "segmento" : mainStocks.get(k)['segmento'],
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
              "p_score" : compute_score(v),
              'cres_5a' : percentageToFloat(v['Cresc.5a'])}\
          )

