import http.client
conn = http.client.HTTPConnection('www.fundamentus.com.br', 80)
conn.request('GET', '/detalhes.php?papel=SMLE3')
res = conn.getresponse()
print(res.status)

data  =res.read()
print(type(data))