#!/usr/bin/env python3

import re
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict

def get_data(*args, **kwargs):
    url = 'http://www.clubefii.com.br/fundos_imobiliarios_ranking'
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    
    with opener.open(url) as link:
        content = link.read().decode('ISO-8859-1')
        print(content)

    pattern = re.compile('<div id="fundos listados".*</div>', re.DOTALL)
    reg = re.findall(pattern, content)[0]
    page = fragment_fromstring(reg)
    lista = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        lista.update({rows.getchildren()[0][0].getchildren()[0].text: {}})
    
    return lista

if __name__ == '__main__':

  print(get_data())
