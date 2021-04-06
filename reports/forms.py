from django import forms
from reports.models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'remark')