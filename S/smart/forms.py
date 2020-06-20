# -*- coding: utf-8 -*-
from django import forms
from splitjson.widgets import SplitJSONWidget


class testForm(forms.Form):
    attrs = {'class': 'form-control input-lg'}
    Results = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=False))