from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from profinfo.models import DynamicsSalaryByYear, DynamicsVacanciesByYear, DynamicsSalaryByYearsForProf, \
    DynamicsVacanciesByYearForProf, SalaryLevelsByCity, FractionVacanciesByCity, TopSkills
import json
import requests
import re
from datetime import datetime, timedelta 

# Create your views here.

def index(request):
    home = {
        'title': 'Fullstack-программист'
    }
    return render(request, 'index.html', home)

def demand(request):
    dem = DynamicsSalaryByYear.objects.all().order_by('year')
    for i in dem:
        i.salary = int(i.salary)
    dem_2 = DynamicsVacanciesByYear.objects.all().order_by('year')
    dem_3 = DynamicsSalaryByYearsForProf.objects.all().order_by('year')
    for i in dem_3:
        i.salary = int(i.salary)
    dem_4 = DynamicsVacanciesByYearForProf.objects.all().order_by('year')
    template = loader.get_template('demand.html')
    context = {
        'saltotal': dem,
        'vactotal': dem_2,
        'salforprof': dem_3,
        'vacforprof': dem_4
    }
    return HttpResponse(template.render(context, request))

def geography(request):
    geog = SalaryLevelsByCity.objects.all().order_by('-salary')
    for i in geog:
        i.salary = int(i.salary)
    geog_2 = FractionVacanciesByCity.objects.all().order_by('-fraction')
    for i in geog_2:
        i.fraction = "{:.2%}".format(i.fraction)
    template = loader.get_template('geography.html')
    context = {
        'vacforcity': geog,
        'vacforcityfrac': geog_2
    }
    return HttpResponse(template.render(context, request))

def skills(request):
    skills_web = TopSkills.objects.filter(year = 0).order_by('-count')
    for i in skills_web:
        i.count = float(i.count)/100
        i.count = "{:.2%}".format(i.count/100)
    skills_all = TopSkills.objects.exclude(year = 0)
    years = sorted(set(str(i.year) for i in skills_all))
    skills_year0 = {}
    for c in range(len(years)):
        sk_year = TopSkills.objects.filter(year = years[c])
        skills_year0[c] = []
        for sk in sk_year:
            skills_year0[c].append((sk.skills.title(), sk.count))
        skills_year0[c].sort(key = lambda el: el[1], reverse = True)
    skills_year = {}
    for r in range(10):
        skills_year[r] = []
        for c in range(len(years)):
            skills_year[r].append(skills_year0[c][r] if skills_year0[c][r] else ('',''))
    template = loader.get_template('skills.html')
    context = {
        'years': years,
        'skills_web': skills_web,
        'skills_year': skills_year
    }
    return HttpResponse(template.render(context, request))

def lastVac(request):
    listKeysForNameVac = ['fullstack', 'full-stack', 'full stack', 'фулстак', 'фуллстак', 'фулстэк', 'фуллстэк']
    res = getLastVacancies(listKeysForNameVac, 10)
    template = loader.get_template('lastVac.html')
    context = {
        'lastVacHeader': res[0],
        'lastTopVacancy': res[1]
    }
    return HttpResponse(template.render(context, request))

def getLastVacancies(listKeysForNameVac, vacCountMax = 10):
    lastVacHeader = [('name','Название вакансии'), ('description', 'Описание вакансии'), ('key_skills', 'Навыки'),
        ('employer', 'Компания'), ('salary', 'Средний Оклад'), ('area','Название региона'), ('published_at', 'Дата публикации вакансии')]
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
        hhlist['published_at'] = format_data(hhlist['published_at'])['date']
        hhlist = [hhlist[h[0]] for h in lastVacHeader]
        hhLastVacTop.append(hhlist)
        vacCount += 1
        if vacCount == vacCountMax: break
    return ([h[1] for h in lastVacHeader], hhLastVacTop)

def format_data(publ):
    t = datetime.strptime(publ[:-5], '%Y-%m-%dT%H:%M:%S')
    dt = timedelta(hours=int(publ[-4:-2]), minutes=int(publ[-2:]))
    utc = t - dt if publ[-5] == '+' else t + dt
    return {'date': f"{datetime.strftime(t, '%d.%m.%Y')} {publ[-13:-5]} {publ[-5:-2]}:{publ[-2:]}:00", 'abs': int(datetime.timestamp(utc))}
    
