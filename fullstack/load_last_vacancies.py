import json
import requests

def getLastVacancies(name):
    req = requests.get('https://api.hh.ru/vacancies', {'text': f'Name: {name}'})
    hhdata = req.content.decode()
    req.close()
    res = []
    for v in json.loads(hhdata)['items'][:10]:
        req = requests.get(v['url'])
        hhdata = req.content.decode()
        req.close()
        res.append(json.loads(hhdata))
    return(res)
    
lastVachh = []
res = getLastVacancies('fullstack')
print(res)
lastVachh.append(res)

xxx = 1