from django import forms
from django.conf import settings
from datetime import datetime
from .models import Request, Client, get_available_dates, get_available_times, get_available_employee


class RequestForm(forms.ModelForm):
    selected_date = forms.DateField(required=True, input_formats=settings.DATE_INPUT_FORMATS)
    selected_time = forms.TimeField(required=True)
    first_name = forms.CharField(required=True)
    phone = forms.RegexField(required=True, regex=r'\d{11}')
    is_accepted = forms.BooleanField(required=True)

    def clean_type(self):
        car = self.cleaned_data.get('car')
        work_type = self.cleaned_data.get('type')
        if car.car.type_id != work_type.car_type_id:
            raise forms.ValidationError('Выбран неверный тип')
        return work_type

    def clean_selected_date(self):
        selected_date = self.cleaned_data.get('selected_date')
        work_type = self.cleaned_data.get('type')
        available_dates = get_available_dates(work_type)
        if selected_date not in available_dates:
            raise forms.ValidationError('Выбранная дата занята. Выберете другое')
        return selected_date

    def clean_selected_time(self):
        selected_time = self.cleaned_data['selected_time']
        selected_date = self.cleaned_data.get('selected_date')
        work_type = self.cleaned_data.get('type')
        available_times = get_available_times(work_type, selected_date)
        if selected_time.strftime(settings.TIME_INPUT_FORMAT) not in available_times:
            raise forms.ValidationError('Выбранное время занято. Выберете другое')
        return selected_time

    def save(self, commit=True):
        self.instance.date = datetime.combine(self.cleaned_data['selected_date'], self.cleaned_data['selected_time'])
        self.instance.client = Client.objects.get_or_create(
            first_name=self.cleaned_data['first_name'],
            phone=self.cleaned_data['phone']
        )[0]
        self.instance.employee = get_available_employee(self.cleaned_data['type'], self.instance.date)
        return super(RequestForm, self).save(commit)

    class Meta:
        model = Request
        fields = ('car', 'type', 'selected_date', 'selected_time', 'first_name', 'phone', 'is_accepted')


class RequestCheckForm(forms.Form):
    id = forms.IntegerField(required=True)
    phone = forms.RegexField(required=True, regex=r'\d{11}')
