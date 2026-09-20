from django import forms

from .models import Category, MenuItem


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
            "description",
        ]


class MenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem

        fields = [
            "category",
            "name",
            "description",
            "price",
            "image",
            "is_available",
        ]