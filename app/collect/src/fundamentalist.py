from fundamentus import fundamentus

if __name__ == '__main__':
    lista = fundamentus.get_data()
    
    print('{0:<7} {1:<7} {2:<10} {3:<7} {4:<10} {5:<7} {6:<10} {7:<10} {8:<10} {9:<11} {10:<11} {11:<7} {12:<11} {13:<14} {14:<7}'.format('Papel',
                                                                                                                                          'Cotação',
                                                                                                                                          'P/L',
                                                                                                                                          'P/VP',
                                                                                                                                          'PSR',
                                                                                                                                          'DY',
                                                                                                                                          'P/EBIT',
                                                                                                                                          'EV/EBIT',
                                                                                                                                          'EBITDA',
                                                                                                                                          'Mrg.Liq.',
                                                                                                                                          'Liq.Corr.',
                                                                                                                                          'ROIC',
                                                                                                                                          'ROE',
                                                                                                                                          'Div.Brut/Pat.',
                                                                                                                                          'Cresc.5a'))
    
    print('-'*154)
    for k, v in lista.items():
        print('{0:<7} {1:<7} {2:<10} {3:<7} {4:<10} {5:<7} {6:<10} {7:<10} {8:<10} {9:<11} {10:<11} {11:<7} {12:<11} {13:<14} {14:<7}'.format(k,
                                                                                                                                              v['cotacao'],
                                                                                                                                              v['P/L'],
                                                                                                                                              v['P/VP'],
                                                                                                                                              v['PSR'],
                                                                                                                                              v['DY'],
                                                                                                                                              v['P/EBIT'],
                                                                                                                                              v['EV/EBIT'],
                                                                                                                                              v['EBITDA'],
                                                                                                                                              v['Mrg.Liq.'],
                                                                                                                                              v['Liq.Corr.'],
                                                                                                                                              v['ROIC'],
                                                                                                                                              v['ROE'],
                                                                                                                                              v['Div.Brut/Pat.'],
                                                                                                                                              v['Cresc.5a']))

