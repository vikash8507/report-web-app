from django import forms

class SalesSearchForm(forms.Form):

    CHART_TYPES = (
        ('#1', 'Bar Chart'),
        ('#2', 'Pie Chart'),
        ('#3', 'Line Chart'),
    )

    RESULTS_TYPES = (
        ('#1', 'Transaction'),
        ('#2', 'Date'),
    )

    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices=CHART_TYPES)
    results_type = forms.ChoiceField(choices=RESULTS_TYPES)