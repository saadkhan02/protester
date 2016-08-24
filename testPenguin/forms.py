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
