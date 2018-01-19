from django import forms
from .models import QuoteModel

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteModel
        fields = ('type_quote', 'first_name', 'last_name', 'name_company', 'email', 'tel_office', 'tel_mobile', 'tel_fax', 'type_product', 'direction', 'detail', 'file_path',  )
