from django.shortcuts import render
from testPenguin.models import Suite, Case, Step
from testPenguin.forms import SuiteForm, CaseForm
import datetime

def welcome(request):
    writeup = "Welcome to test penguin. Automated testing simlified."
    content = {'writeup': writeup}

    return render(request, 'testPenguin/welcome.html', content)

def dashboard(request):
    return render(request, 'testPenguin/dashboard.html')

def login(request):
    return render(request, 'testPenguin/login.html')

def testSuites(request):
    form = SuiteForm()

    if (request.method == 'POST'):
        form = SuiteForm(request.POST)
        if (not form.is_valid()):
            print(form.errors)
        else:
            suite = form.save(commit=False)
            suite.suite_created = datetime.datetime.now()
            suite.suite_modified = datetime.datetime.now()
            suite.save()

    suiteList = Suite.objects.order_by("suite_created")
    content = {'form': form, 'suiteList': suiteList}

    return render(request, 'testPenguin/testSuites.html', content)

def testCases(request):
    form = CaseForm()

    if (request.method == 'POST'):
        form = CaseForm(request.POST)
        if (not form.is_valid()):
            print(form.errors)
        else:
            case = form.save(commit=False)
            case.case_created = datetime.datetime.now()
            case.case_modified = datetime.datetime.now()
            case.save()

    caseList = Case.objects.order_by("case_created")
    content = {'form': form, 'caseList': caseList}

    return render(request, 'testPenguin/testCases.html', content)
