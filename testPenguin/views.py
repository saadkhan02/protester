from django.shortcuts import render
from testPenguin.models import Suite, Case, Step
from testPenguin.forms import SuiteForm, CaseForm, testSuiteDetailsForm
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
        if ('del' in request.POST):
            Suite.objects.get(suite_slug = request.POST['del']).delete()
        else:
            form = SuiteForm(request.POST)
            if (not form.is_valid()):
                print(form.errors)
            else:
                suite = form.save(commit=False)
                suite.suite_created = datetime.datetime.now()
                suite.suite_modified = datetime.datetime.now()
                suite.save()
                form = SuiteForm()

    suiteList = Suite.objects.order_by("suite_created")
    content = {'form': form, 'suiteList': suiteList}

    return render(request, 'testPenguin/testSuites.html', content)

def testSuiteDetails(request, suite_name_slug):
    suite = Suite.objects.get(suite_slug = suite_name_slug)
    error = "no error"
    form = testSuiteDetailsForm()
    if (request.method == 'POST'):
        form = testSuiteDetailsForm(request.POST)
        if (form.is_valid()):
            if ('addCase' in request.POST):
                try:
                    case = Case.objects.get(case_name =
                        form.cleaned_data['caseSelection'])
                    suite.case_set.add(case)
                    suite.save()
                    form = testSuiteDetailsForm()
                except:
                    Case.DoesNotExist
            else:
                error = "the post was delivered"
                try:
                    case = Case.objects.get(case_name = request.POST['delCase'])
                    error = request.POST['delCase']
                    suite.case_set.remove(case)
                    suite.save()
                    form = testSuiteDetailsForm()
                except:
                    Case.DoesNotExist

    suiteCases = suite.case_set.all()
    content = {'suite': suite,
        'form': form,
        'error': error,
        'suiteCases': suiteCases}

    return render(request, 'testPenguin/testSuiteDetails.html', content)

def testCases(request):
    form = CaseForm()

    if (request.method == 'POST'):
        form = CaseForm(request.POST)
        if (not form.is_valid()):
            print(form.errors)
        else:
            if (request.value == 'save'):
                case = form.save(commit=False)
                case.case_created = datetime.datetime.now()
                case.case_modified = datetime.datetime.now()
                case.save()
                form = CaseForm()

    caseList = Case.objects.order_by("case_created")
    content = {'form': form, 'caseList': caseList}

    return render(request, 'testPenguin/testCases.html', content)
