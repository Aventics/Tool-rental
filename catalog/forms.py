from django import forms
    
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.

class RenewToolForm(forms.Form):
    renewal_date = forms.DateField(help_text="Введите дату возврата инструмента (от сегодня до 4-х недель).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(('Не верная дата. Число не может быть меньше сегодняшнего'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(('Не верная дата. Число не может быть больше чем через 4 недели'))

        return data