from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from testPenguin.models import Suite, Case, Step
from testPenguin.forms import SuiteForm, CaseForm, testSuiteDetailsForm, \
    testCaseDetailsForm, modifyCaseForm
import datetime

##
# Welcome view
#
# @param request Page request.
#
def welcome(request):
    writeup = "Welcome to test penguin. Automated testing simlified."
    content = {'writeup': writeup}

    return render(request, 'testPenguin/welcome.html', content)

##
# Dashboard view
#
# @param request Page request.
#
def dashboard(request):
    return render(request, 'testPenguin/dashboard.html')

##
# Login view
#
# @param request Page request.
#
def login(request):
    return render(request, 'testPenguin/login.html')

##
# Test suite view
#
# This covers the page used to add and display all available test suites.
#
# @param request Page request.
#
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

##
# Adds a case to a suite.
#
# @param suite Suite object to which cases will be added.
# @param request POST request sent with the form.
# @param error Error descriptor meant for debugging.
#
def addCaseToSuite(suite, request, error):
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

    return error

##
# Modify suite details.
#
# Modifies the suite details - name and description.
#
# @param suite Suite object that needs modification.
# @param request POST request sent with the form.
# @param error Error descriptor meant for debugging.
#
def modifySuiteDetails(suite, request, error):
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

    return error

##
# Test suite details view
#
# This covers the page that adds, displays and edits all cases of a suite.
#
# @param request POST request sent with the form.
# @param suite_name_slug Suite name slug to identify the suite in use.
#
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

            return HttpResponseRedirect('/testPenguin/testSuites/' + \
                suite.suite_slug + '/')

        if ('addButton' in request.POST):
            error = addCaseToSuite(suite, request, error)

        if ('modifyButton' in request.POST):
            error = modifySuiteDetails(suite, request, error)

    suiteCases = suite.case_set.all()
    content = {'suite': suite,
        'form': form,
        'error': error,
        'suiteCases': suiteCases}

    return render(request, 'testPenguin/testSuiteDetails.html', content)

##
# Add steps to case
#
# Adds steps to a specific case.
#
# @param request POST request sent with the form.
# @param case Case object in use.
#
def addStepsToCase(request, case):
    error = "Add button was pressed"
    form = testCaseDetailsForm(request.POST)
    if (form.is_valid()):
        error = "Form is valid"
        try:
#           Add validations
            maxStepOrder = 0
            try:
                maxStepOrder = case.step_set.order_by('step_order'). \
                    step_order
            except:
                maxStepOrder = 0
                error = "This is going to be the first step"

                case.step_set.create(
                step_name = form.cleaned_data['stepName'],
                action = form.cleaned_data['action'],
                step_order = maxStepOrder + 1,
                always_run = form.cleaned_data['alwaysRun'],
                locator_type = form.cleaned_data['locatorType'],
                locator = form.cleaned_data['locator'],
                value = form.cleaned_data['value'])
            case.save()
            return HttpResponseRedirect('/testPenguin/testCases/' + \
                case.case_slug + '/')
        except:
            error = "incomplete information"

    return error

##
# Test case details view.
#
# This covers the page that adds, displays and edits all steps of a test case.
#
# @param request POST resquest sent with the form
# @param case_name_slug Case name slug to identify the case in use
#
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

        if ('addButton' in request.POST):
            error = addStepsToCase(request, case)

        if ('removeButton' in request.POST):
            form = testCaseDetailsForm(request.POST)
            if (form.is_valid()):
                step = case.step_set.get(pk = request.POST['removeButton'])
                step.delete()
                case.save()

                return HttpResponseRedirect('/testPenguin/testCases/' + \
                    case.case_slug + '/')

#        if ('upButton' in request.POST):
#            form = testCaseDetailsForm(request.POST):
#            if (form.is_valid()):
#                currentOrder = case.step_set.
#                    get(pk = request.POST['upButton']).step_order

    caseSteps = case.step_set.all()
    content = {'case': case,
        'caseSteps': caseSteps,
        'form': form,
        'error': error}

    return render(request, 'testPenguin/testCaseDetails.html', content)

##
# Modify case view
#
# This covers case modification for a specific case.
#
# @param request POST request sent with the form.
# @param case_name_slug Slugified case name used to identify the case in use.
#
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

##
# Test cases view.
#
# Displayes the list of test cases available. Also provides a means of adding,
# deleting and modifying them.
#
# @param request POST request sent with the form.
#
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
