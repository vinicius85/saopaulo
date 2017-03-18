from fundamentus import fundamentus
from elasticsearch import Elasticsearch
from datetime import datetime

def percentageToFloat(value):
  return float(value.replace('%','').replace(',','.'))

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

def load_my_stocks(filename):
  dict = {}
  companies = [line.strip() for line in open(filename, 'r')]
  for company in companies:
    companyData = company.split(';')
    dict.update({companyData[0]:{
                                 'posicao':     int(companyData[1]),
                                 'preco_compra': float(companyData[2]),
                                 'data_inicio': companyData[3],
                                 'data_aporte': companyData[4]}})
  return dict


def compute_score(att):
  p_vpa = percentageToFloat(att['P/VP']) 
  d_y = percentageToFloat(att['DY']) 
  roe = percentageToFloat(att['ROE']) 
  return   (- 10 * p_vpa) + (2 * d_y) + roe

def rentabilidade(cotacaoEntrada,cotacaoAtual):
  return round(((cotacaoAtual/cotacaoEntrada)-1),2)
         


if __name__ == '__main__':

    es = Elasticsearch()
    es.indices.create(index='fundamental', ignore=400)

    mainStocks = load_companies_info('/home/vinicius/workspace/saopaulo/app/collect/res/empresas.txt')
    myStocks = load_my_stocks('/home/vinicius/workspace/saopaulo/app/collect/res/carteira.txt')
    lista = fundamentus.get_data()

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
              "posicao" :  myStocks.get(k)['posicao'] if myStocks.get(k) is not None else 0,
              "posicao_total" :  myStocks.get(k)['posicao']*percentageToFloat(v['cotacao']) if myStocks.get(k) is not None else 0.0,
              "preco_compra" :  myStocks.get(k)['preco_compra'] if myStocks.get(k) is not None else 0.0,
              "data_inicio" : datetime.strptime(myStocks.get(k)['data_inicio'],'%d/%m/%Y') if myStocks.get(k) is not None else None,
              "data_aporte" : datetime.strptime(myStocks.get(k)['data_aporte'],'%d/%m/%Y') if myStocks.get(k) is not None else None,
              "rent" : rentabilidade(myStocks.get(k)['preco_compra'],percentageToFloat(v['cotacao'])) if myStocks.get(k) else 0.0,
              'cres_5a' : percentageToFloat(v['Cresc.5a'])}\
          )

