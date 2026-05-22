from django import forms
from .models import Collection

class CollectionForm(forms.ModelForm):
    """
    Form used for creating or updating a Collection instance.
    """
    class Meta:
        model = Collection
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional description of the collection.'})
        }
        # Custom validation methods
        def clean_name(self):
            name = self.cleaned_data.get('name')
            if name and name.lower() == 'placeholder':
                raise forms.ValidationError("Collection name cannot be 'Placeholder'.'")
            return name
