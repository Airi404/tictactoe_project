from django import forms

class ChatForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Escribe tu consulta aquí...'
        })
    )