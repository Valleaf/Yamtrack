from django import forms
from django_select2 import forms as s2forms

from collections.models import Collection


class CollaboratorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["username__icontains"]


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "description", "collaborators"]
        widgets = {
            "collaborators": CollaboratorsWidget(
                attrs={
                    "data-minimum-input-length": 1,
                    "data-placeholder": "Search users...",
                    "data-allow-clear": "false",
                }
            )
        }
