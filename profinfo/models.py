from django.db import models

# Create your models here.

class DynamicsSalaryByYear(models.Model):
    year = models.IntegerField('Год')
    salary = models.FloatField('Зарплата')

class DynamicsVacanciesByYear(models.Model):
    year = models.IntegerField('Год')
    vacancy = models.TextField('Вакансия')
    
class DynamicsSalaryByYearsForProf(models.Model):
    year = models.IntegerField('Год')
    salary = models.FloatField('Зарплата')

class DynamicsVacanciesByYearForProf(models.Model):
    year = models.IntegerField('Год')
    vacancy = models.TextField('Вакансия')
    
class SalaryLevelsByCity(models.Model):
    city = models.TextField('Город')
    salary = models.FloatField('Зарплата')

class FractionVacanciesByCity(models.Model):
    city = models.TextField('Город')
    fraction = models.FloatField('Доля')

class TopSkills(models.Model):
    skills = models.TextField('Название')
    year = models.IntegerField('Год')
    count = models.IntegerField('Количество повторений')
