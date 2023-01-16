from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from profinfo.models import DynamicsSalaryByYear, DynamicsVacanciesByYear, DynamicsSalaryByYearsForProf, \
    DynamicsVacanciesByYearForProf, SalaryLevelsByCity, FractionVacanciesByCity, TopSkills
import json
import requests

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
    numb = [i for i in range(10)]
    skills_year0 = {}
    for yr in years:
        skills_year0[yr] = {}
        n = 0
        for j in TopSkills.objects.filter(year = yr).order_by('-count'):
            if n == 10: break
            skills_year0[yr][str(n)] = (j.skills, j.count)
            n += 1
    skills_year = {}
    for n in numb:
        skills_year[str(n)] = (skills_year0[years[0]][str(n)][0],skills_year0[years[0]][str(n)][1],skills_year0[years[1]][str(n)][0],skills_year0[years[1]][str(n)][1],
                          skills_year0[years[2]][str(n)][0],skills_year0[years[2]][str(n)][1],skills_year0[years[3]][str(n)][0],skills_year0[years[3]][str(n)][1],
                          skills_year0[years[4]][str(n)][0],skills_year0[years[4]][str(n)][1],skills_year0[years[5]][str(n)][0],skills_year0[years[5]][str(n)][1],
                          skills_year0[years[6]][str(n)][0],skills_year0[years[6]][str(n)][1],skills_year0[years[7]][str(n)][0],skills_year0[years[7]][str(n)][1])
    template = loader.get_template('skills.html')
    context = {
        'numb': numb,
        'years': years,
        'skills_web': skills_web,
        'skills_year': skills_year,
    }
    return HttpResponse(template.render(context, request))

def lastVac(request):
    req = requests.get('https://api.hh.ru/vacancies', {'text': 'Name: fullstack'})
    hhdata = req.content.decode()
    req.close()
    res = []
    for v in json.loads(hhdata)['items'][:10]:
        req = requests.get(v['url'])
        hhdata = req.content.decode()
        req.close()
        res.append(json.loads(hhdata))
    
    print(res)
    
    template = loader.get_template('lastVac.html')
    context = {
        'last_vacancy': res
    }
    return HttpResponse(template.render(context, request))

