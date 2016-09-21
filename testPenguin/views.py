from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from testPenguin.models import Suite, Case, Step
from testPenguin.forms import SuiteForm, CaseForm, testSuiteDetailsForm, \
    testCaseDetailsForm, modifyCaseForm
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
    redirectString = '/testPenguin/testSuites/' + suite.suite_slug + '/'
    error = "no error"
    form = testSuiteDetailsForm()
    if (request.method == 'POST'):
        error = "The request method is post"
        if ('removeButton' in request.POST):
            error = "You have cliked the REMOVE button."
            suite.case_set.remove(Case.objects.get(case_name =
                request.POST['removeButton']))
            form = testSuiteDetailsForm()

            return HttpResponseRedirect('/testPenguin/testSuites/' + \
                suite.suite_slug + '/')

        if ('addButton' in request.POST):
            error = "You have clicked the ADD button."
            form = testSuiteDetailsForm(request.POST)
            if (form.is_valid()):
                error = "Form is valid"
                try:
                    case = Case.objects.get(case_name =
                        form.cleaned_data['caseSelection'])
                    suite.case_set.add(case)
                    suite.save()
                    form = testSuiteDetailsForm()

                    return HttpResponseRedirect('/testPenguin/testSuites/' + \
                        suite.suite_slug + '/')
                except:
                    Case.DoesNotExist

        if ('modifyButton' in request.POST):
            error = "You have clicked the MODIFY button."
            form = testSuiteDetailsForm(request.POST)
            if (form.is_valid()):
                error = "Form is valid"
                try:
                    if (not(form.cleaned_data['suiteName'] == suite.suite_name)
                        and not(form.cleaned_data['suiteName'] == '')):
                        suite.suite_name = form.cleaned_data['suiteName']
                        suite.save()
                    if (not(form.cleaned_data['suiteDescription'] ==
                        suite.suite_description)
                        and not(form.cleaned_data['suiteDescription'] == '')):
                        suite.suite_description = \
                            form.cleaned_data['suiteDescription']
                        suite.save()

                    return HttpResponseRedirect('/testPenguin/testSuites/' + \
                        suite.suite_slug + '/')
                except:
                    Case.DoesNotExist

    suiteCases = suite.case_set.all()
    content = {'suite': suite,
        'form': form,
        'error': error,
        'suiteCases': suiteCases}

    return render(request, 'testPenguin/testSuiteDetails.html', content)

def testCaseDetails(request, case_name_slug):
    case = Case.objects.get(case_slug = case_name_slug)
    form = testCaseDetailsForm()
    error = "no error as of now"
    if (request.method == 'POST'):
        error = "The method is post"
        if ('modifyButton' in request.POST):
            error = "button was pressed"
            return HttpResponseRedirect('/testPenguin/testCases/' + \
                case.case_slug + '/modifyCase/')

    content = {'case': case,
        'form': form,
        'error': error}

    return render(request, 'testPenguin/testCaseDetails.html', content)

def modifyCase(request, case_name_slug):
    case = Case.objects.get(case_slug = case_name_slug)
    form = modifyCaseForm(initial = {'caseName': case.case_name,
        'caseDescription': case.case_description})
    error = "No error as of now."
    if (request.method == 'POST'):
        error = "The method is post"
        if ('modifyCaseDetails' in request.POST):
            error = "You have clicked the MODIFY button."
            form = modifyCaseForm(request.POST)
            if (form.is_valid()):
                error = "Form is valid"
                try:
                    if (not(form.cleaned_data['caseName'] == case.case_name)
                        and not(form.cleaned_data['caseName'] == '')):
                        case.case_name = form.cleaned_data['caseName']
                        case.save()
                    if (not(form.cleaned_data['caseDescription'] ==
                        case.case_description)
                        and not(form.cleaned_data['caseDescription'] == '')):
                        case.case_description = \
                            form.cleaned_data['caseDescription']
                        case.save()

                    return HttpResponseRedirect('/testPenguin/testCases/' + \
                        case.case_slug + '/')
                except:
                    Case.DoesNotExist

    content = {'case': case,
        'form': form,
        'error': error
    }

    return render(request, 'testPenguin/modifyCase.html', content)

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
            form = CaseForm()

    caseList = Case.objects.order_by("case_created")
    content = {'form': form, 'caseList': caseList}

    return render(request, 'testPenguin/testCases.html', content)
