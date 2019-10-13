from django import forms


class EventCreationForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(max_length=2048)
    contact = forms.CharField(max_length=64)
    location = forms.CharField(max_length=64)
    spots = forms.CharField(max_length=16)
    is_public = forms.BooleanField()
    time = forms.CharField(max_length=64)


class EventAddVolunteersForm(forms.Form):
    email = forms.CharField(
        max_length=64,
        label='Enter a singular email: ',
        required=False,
    )
    emails = forms.CharField(
        max_length=256,
        label='Or enter a list of emails! Please seperate them by spaces or commas: ',
        widget=forms.Textarea,
        required=False,
    )

# This is a dummy form so we can use FormView in our views.py. While we simply just have a single submit button,
# by using a form, we can call def form_valid() when it is over, which lets our apply database modifications.
# Admitedly, this is a very hacky method, but for the sake of time I am doing this.
class EventEmptyForm(forms.Form):
    pass
