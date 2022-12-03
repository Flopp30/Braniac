from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError


# from django import forms

# class StyleFormMixin: # || аналог crispy
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             if isinstance(field.widget, forms.widgets.CheckboxInput):
#                 field.widget.attrs['class'] = 'form-check-input'
#             elif isinstance(field.widget, forms.DateTimeInput):
#                 field.widget.attrs['class'] = 'form-control flatpickr-basic'
#             if isinstance(field.widget, forms.TimeInput):
#                 field.widget.attrs['class'] = 'form-control flatpickr-time'
#             if isinstance(field.widget, forms.widgets.SelectMultiple):
#                 field.widget.attrs['class'] = 'select2 form-control select2-multiple'
#             else:
#                 field.widget.attrs['class'] = 'form-control'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('Вы слишком молоды для регистрации. Приходите с родителями :)')
        return age


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('Вы слишком молоды для регистрации. Приходите с родителями :)')
        return age
