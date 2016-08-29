from django.db import models
from django.template.defaultfilters import slugify
import datetime

class Suite(models.Model):
    suite_name = models.CharField(max_length=128, unique=True)
    suite_description = models.CharField(max_length=500)
    suite_created = models.DateTimeField("Date created")
    suite_modified = models.DateTimeField("Date modified")
    suite_slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.suite_slug = slugify(self.suite_name)
        self.suite_modified = datetime.datetime.now()
        super(Suite, self).save(*args, **kwargs)

    def __str__(self):
        return self.suite_name

class Schedule(models.Model):
    suite = models.ForeignKey(Suite)
    day_of_month = models.IntegerField()
    day_of_week = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = 'schedule'

class timeOfDay(models.Model):
    schedule = models.ForeignKey(Schedule)
    timeOfDay = models.IntegerField()

class Case(models.Model):
    suite = models.ManyToManyField(Suite, blank=True)
    case_name = models.CharField(max_length=128, unique=True)
    case_description = models.CharField(max_length=500)
    case_created = models.DateTimeField("Date created")
    case_modified = models.DateTimeField("Date modified")
    case_slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.case_slug = slugify(self.case_name)
        super(Case, self).save(*args, **kwargs)

    def __str__(self):
        return self.case_name

class Step(models.Model):
    case = models.ForeignKey(Case)
    step_name = models.CharField(max_length=128, unique=True)
    step_created = models.DateTimeField("Date created")
    step_modified = models.DateTimeField("Date modified")
    step_slug = models.SlugField(unique=True)
    always_run = models.IntegerField(default=0)
    action = models.CharField(max_length=128)
    arg1 = models.CharField(max_length=128)
    arg2 = models.CharField(max_length=128)
    arg3 = models.CharField(max_length=128)
    message = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.step_slug = slugify(step_name)
        super(Step, self).save(*args, **kwargs)

    def __str__(self):
        return self.step_name
