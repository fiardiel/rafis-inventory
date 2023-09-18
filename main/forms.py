from django.forms import ModelForm
from main.models import Items

class ProductForm(ModelForm):
    class Meta:
        model = Items
        fields = ["name", "amount", "description", "category", "damage"]