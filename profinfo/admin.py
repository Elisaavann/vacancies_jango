from django.contrib import admin
from profinfo.models import DynamicsSalaryByYear, DynamicsVacanciesByYear, DynamicsSalaryByYearsForProf, \
     DynamicsVacanciesByYearForProf, SalaryLevelsByCity, FractionVacanciesByCity, TopSkills

admin.site.register(DynamicsSalaryByYear)
admin.site.register(DynamicsVacanciesByYear)
admin.site.register(DynamicsSalaryByYearsForProf)
admin.site.register(DynamicsVacanciesByYearForProf)
admin.site.register(SalaryLevelsByCity)
admin.site.register(FractionVacanciesByCity)
admin.site.register(TopSkills)

