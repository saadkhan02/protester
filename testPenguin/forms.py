from django import forms
import datetime
from testPenguin.models import Suite, Case, Step


class SuiteForm(forms.ModelForm):
    suite_name = forms.CharField(max_length = 128, help_text = "Suite Name")
    suite_description = forms.CharField(max_length = 500,
        help_text = "Description", widget = forms.Textarea)
    suite_created = forms.DateTimeField(widget = forms.HiddenInput(),
        initial = datetime.datetime.now())
    suite_modified = forms.DateTimeField(widget = forms.HiddenInput(),
        initial = datetime.datetime.now())
    suite_slug = forms.CharField(widget = forms.HiddenInput(), required = False)

    class Meta:
        model = Suite
        fields = ('suite_name', 'suite_description')

class CaseForm(forms.ModelForm):
    case_name = forms.CharField(max_length = 128, help_text = "Case Name")
    case_description = forms.CharField(max_length = 500,
        help_text = "Description", widget = forms.Textarea)
    case_created = forms.DateTimeField(widget = forms.HiddenInput(),
        initial = datetime.datetime.now())
    case_modified = forms.DateTimeField(widget = forms.HiddenInput(),
        initial = datetime.datetime.now())
    case_slug = forms.CharField(widget = forms.HiddenInput(), required = False)

    class Meta:
        model = Case
        fields = ('case_name', 'case_description')
        exclude = ('suite',)

def getCaseList():
    cases = Case.objects.all()
    caseNameList = []
    caseNameList.append(["Select a case", "Select a case"])
    for case in cases:
        caseNameList.append([case.case_name, case.case_name])

    return caseNameList

class testSuiteDetailsForm(forms.Form):
    suiteName = forms.CharField(max_length = 128, required = False)
    suiteDescription = forms.CharField(max_length = 500,
        widget =  forms.Textarea, required = False)

    def __init__(self, *args, **kwargs):
        super(testSuiteDetailsForm, self).__init__(*args, **kwargs)
        self.fields['caseSelection'] = \
            forms.ChoiceField(choices = getCaseList(), required = False)

# We make the action list dynamically available so that we can add more actions
# without having to restart the webserver.
def getActionList():
    actions = []
    actions.append(["", "Select an action"])
    actions.append(["Browse", "Browse"])
    actions.append(["Click", "Click"])
    actions.append(["Select", "Select"])
    actions.append(["Input", "Input"])
    actions.append(["Select with input", "Select with input"])

    return actions

# We make the locator type list dynamically available so that we can add more
# locator types without having to restart the webserver.
def getLocatorTypes():
    locatorTypes = []
    locatorTypes.append(["", "Select Locator Type"])
    locatorTypes.append(["id", "id"])
    locatorTypes.append(["xpath", "xpath"])
    locatorTypes.append(["name", "name"])
    locatorTypes.append(["css", "css"])
    locatorTypes.append(["text", "text"])

    return locatorTypes

class testCaseDetailsForm(forms.Form):
    alwaysRunOptions = []
    alwaysRunOptions.append(["False", "False"])
    alwaysRunOptions.append(["True", "True"])
    actions = getActionList()

    action = forms.ChoiceField(choices = actions, required = False)
    stepName = forms.CharField(max_length = 128, required = False)
    alwaysRun = forms.ChoiceField(choices = alwaysRunOptions,
        required = False)
    locatorType = forms.ChoiceField(choices = getLocatorTypes(),
        required = False)
    locator = forms.CharField(max_length = 200, required = False)
    value = forms.CharField(max_length = 200, required = False)

class modifyCaseForm(forms.Form):
    caseName = forms.CharField(max_length = 128, required = False)
    caseDescription = forms.CharField(max_length = 500,
        widget = forms.Textarea, required = False)
