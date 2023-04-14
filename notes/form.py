from django import forms


class AddNoteForm(forms.Form):
    note = forms.CharField(label='note')

class MoveNoteForm(forms.Form):
    note = forms.IntegerField()