from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms

from dsbd.ticket.models import Ticket

class TicketInitForm(forms.Form):
    ticket_type = forms.fields.ChoiceField(
        label='チケットの種別(User or Group)を選んでください',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['type1', 'type2', 'title', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type1'].widget.attrs['readonly'] = True
        self.fields['type2'].widget.attrs['readonly'] = True

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
