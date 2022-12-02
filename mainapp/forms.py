from django import forms

from mainapp.models import CourseFeedback


class CourseFeedBackForm(forms.ModelForm):

    def __init__(self, *args, course=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if course and user:
            self.fields['course'].initial = course.pk
            self.fields['user'].initial = user.pk

    class Meta:
        model = CourseFeedback
        fields = ('course', 'user', 'rating', 'feedback')
        widgets = {
            'course': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }
