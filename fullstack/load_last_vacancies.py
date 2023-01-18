import json
import requests
import re
from datetime import datetime, timedelta 

def getLastVacancies(listKeysForNameVac, vacCountMax = 10):
    lastVacHeader = [('name','Название вакансии'), ('description', 'Описание вакансии'),
        ('key_skills', 'Навыки'), ('employer', 'Компания'), ('salary', 'Средний Оклад'),
        ('area','Название региона'), ('published_at', 'Дата публикации вакансии')]
    hhlistfull = []
    hhlist_id = []
    for keyForNameVac in listKeysForNameVac:
        req = requests.get('https://api.hh.ru/vacancies?text=NAME:' + keyForNameVac)
        hhdata = req.content.decode()
        req.close()
        hhlist = json.loads(hhdata)['items']
        for v in hhlist:
            if ((v['id'] not in hhlist_id) and 
                    ((v['type']['id'] == 'open') or (v['type']['name'] == 'Открытая'))):
                hhlist_id.append(v['id'])
                hhlistfull.append(v)
    hhlistfull.sort(key=lambda v: format_data(v['published_at'])['abs'], reverse=True)
    hhLastVacTop = []
    vacCount = 0
    for v in hhlistfull:
        req = requests.get(v['url'])
        hhdata = req.content.decode()
        req.close()
        hhlist = json.loads(hhdata)
        hhlist['description'] = ' '.join(re.sub(r'\<[^>]*\>', '', hhlist['description']).split()) 
        hhlist['key_skills'] = ', '.join([ks['name'] for ks in hhlist['key_skills']])
        hhlist['employer'] = hhlist['employer']['name']
        if hhlist['salary'] == None: continue
        hhlist['salary']['to'] = hhlist['salary']['from'] if hhlist['salary']['to'] == None else hhlist['salary']['to']
        hhlist['salary']['from'] = hhlist['salary']['to'] if hhlist['salary']['from'] == None else hhlist['salary']['from']
        if hhlist['salary']['from'] == None: continue
        hhlist['salary']['currency'] = 'RUR' if hhlist['salary']['currency'] == None else hhlist['salary']['currency']
        hhlist['salary'] = f"{int((float(hhlist['salary']['from']) + float(hhlist['salary']['to']))/2)} {hhlist['salary']['currency']}" 
        hhlist['area'] = hhlist['area']['name']
        hhlist = [hhlist[h[0]] for h in lastVacHeader]
        hhLastVacTop.append(hhlist)
        vacCount += 1
        if vacCount == vacCountMax: break
    return ([h[1] for h in lastVacHeader], hhLastVacTop)

def format_data(publ):
    t = datetime.strptime(publ[:-5], '%Y-%m-%dT%H:%M:%S')
    dt = timedelta(hours=int(publ[-4:-2]), minutes=int(publ[-2:]))
    utc = t - dt if publ[-5] == '+' else t + dt
    return {'date': ' '.join(publ.split('T')), 'abs': int(datetime.timestamp(utc))}
    
res = getLastVacancies(['fullstack', 'full-stack', 'full stack', 'фулстак', 'фуллстак', 'фулстэк', 'фуллстэк'], 10)
print(res[0])
print(res[1])


xxx = 1


