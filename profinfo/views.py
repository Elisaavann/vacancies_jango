#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from profinfo.models import DynamicsSalaryByYear, DynamicsVacanciesByYear, DynamicsSalaryByYearsForProf, \
    DynamicsVacanciesByYearForProf, SalaryLevelsByCity, FractionVacanciesByCity, TopSkills

# Create your views here.

def index(request):
    home = {
        'title': 'Fullstack-программист'
    }
    return render(request, 'index.html', home)


def demand(request):
    dem = DynamicsSalaryByYear.objects.all()
    for i in dem:
        i.salary = int(i.salary)
    dem_2 = DynamicsVacanciesByYear.objects.all()
    dem_3 = DynamicsSalaryByYearsForProf.objects.all()
    for i in dem_3:
        i.salary = int(i.salary)
    dem_4 = DynamicsVacanciesByYearForProf.objects.all()

    # print(dem)
    # print(dem_2)
    # print(dem_3)
    # print(dem_4)

    template = loader.get_template('demand.html')
    context = {
        'saltotal': dem,
        'vactotal': dem_2,
        'salforprof': dem_3,
        'vacforprof': dem_4
    }
    return HttpResponse(template.render(context, request))

def geography(request):
    geog = SalaryLevelsByCity.objects.all()
    for i in geog:
        i.salary = int(i.salary)
    geog_2 = FractionVacanciesByCity.objects.all()
    for i in geog_2:
        i.fraction = "{:.2%}".format(i.fraction)
    
    #print(geog)
    #print(geog_2)

    template = loader.get_template('geography.html')
    context = {
        'vacforcity': geog,
        'vacforcityfrac': geog_2
    }
    return HttpResponse(template.render(context, request))

def skills(request):
    skill = TopSkills.objects.all()

    #print(skill)

    template = loader.get_template('skills.html')
    context = {
        'skill': skill
    }
    return HttpResponse(template.render(context, request))

def lastVac(request):
    return render(request, 'lastVac.html')
