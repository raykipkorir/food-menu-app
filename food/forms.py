from django import forms

from .models import Food


class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ("name", "food_pic", "price", "category")
